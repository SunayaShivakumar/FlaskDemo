from flask import render_template, redirect, url_for, jsonify, request
from app import app, db
from .models import Picture, Survey, Useroutfits
from .forms import surveyForm, outfitForm
import json
import os, operator
import pickle
import numpy as np
​
​
LOCAL_MALLET_APP = "mallet-2.0.8RC3/bin/mallet"
​
topics = None
items = None
phiMatrices = None
topItemsByTopic = None
​
​
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
​
	if request.method == "POST":
		global topics
		global items
		global phiMatrices
		global topItemsByTopic
		topics, items, phiMatrices, topItemsByTopic = getTopics()
		return "done"
	return render_template("index.html")
​
@app.route('/page1', methods=['GET','POST'])
def survey_page1():
	# form = outfitcollection()
	form = outfitForm()
​
	return render_template('page1.html', form=form)
​
@app.route('/page11', methods=['GET','POST'])
def handle_survey_page1():
	
	form = outfitForm(request.form)
	# if form.validate_on_submit():
		# outfits = useroutfits(outfit_one=form.outfit_one.data, outfit_two=form.outfit_two.data, outfit_three=form.outfit_three.data)
	outfits = Useroutfits(outfit_one=form.outfit_one.data, outfit_two=form.outfit_two.data, outfit_three=form.outfit_three.data)
	db.session.add(outfits)
	db.session.commit()
​
	comp_str = form.outfit_one.data+" "+form.outfit_two.data+" "+form.outfit_three.data
​
	file_saver_local("concrete", comp_str)
	mallet_runner_local("concrete")
	# file_saver_AWS("concrete", comp_str)
	# mallet_runner_AWS("concrete")
​
	global topics
	global phiMatrices
​
	topItemsByStyleWord = getItemsByStyle(topics,phiMatrices,"concrete")
	print(topItemsByStyleWord)
	return jsonify(topItemsByStyleWord)
​
​
@app.route('/page3', methods=['GET','POST'])
def survey_page3():
	form = surveyForm()
​
	return render_template('page3.html', form=form)
​
@app.route('/page31', methods=['POST','GET'])
def handle_survey_page3():
	print(request.form)
	form = surveyForm(request.form)
	print(form.event.data)
	survey_result = Survey(event=form.event.data,
							location=form.location.data,
							weather=form.weather.data,
							style=form.style.data)
	db.session.add(survey_result)
	db.session.commit()
​
	comp_str = form.event.data+" "+form.location.data+" "+form.weather.data+" "+form.style.data
	file_saver_local("abstract", comp_str)
	mallet_runner_local("abstract")
​
	global topics
	global phiMatrices
​
	topItemsByStyleWord = getItemsByStyle(topics,phiMatrices,"abstract")
	print(topItemsByStyleWord)
	# return jsonify(doctops_return)
	return jsonify(topItemsByStyleWord)
​
​
@app.route('/thankyou', methods=['GET','POST'])
def thankyou():
	return render_template("thankpage.html")
​
def file_saver_local(AorC, str):
	if AorC == "concrete":
		with open("app/mallet/concrete_words.txt", "w") as f:
			f.write(str)
	else:
		with open("app/mallet/abstract_words.txt", "w") as f:
			f.write(str)
​
​
def mallet_runner_local(AorC):
	command1 = "mallet-2.0.8RC3/bin/mallet import-file --input app/mallet/concrete_words.txt --output app/mallet/concrete_out.sequences --keep-sequence --token-regex '[\p{L}\p{P}\p{N}]*\p{L}' --use-pipe-from app/mallet/concrete.sequences"
	command2 = "mallet-2.0.8RC3/bin/mallet infer-topics --input app/mallet/concrete_out.sequences --inferencer app/mallet/inferencer-1.output.0 --output-doc-topics app/mallet/c2adoctops"
​
	command3 = "mallet-2.0.8RC3/bin/mallet import-file --input app/mallet/abstract_words.txt --output app/mallet/abstract_output.sequences --keep-sequence --token-regex '[\p{L}\p{P}\p{N}]*\p{L}' --use-pipe-from app/mallet/abstract.sequences"
	command4 = "mallet-2.0.8RC3/bin/mallet infer-topics --input app/mallet/abstract_output.sequences --inferencer app/mallet/inferencer-1.output.1 --output-doc-topics app/mallet/a2cdoctops"
​
	if AorC == "concrete":
		os.system(command1)
		print("done")
		os.system(command2)
		print("done2")
​
	else:
		os.system(command3)
		print("done3")
		os.system(command4)
		print("done4")
	return
​
def dataPreprocessing(labels,keyfile,wordweightfile):
    topics = {}
    with open(keyfile) as f:
        for lines in f:
            if len(lines.split('\t')) == 2:
                data = lines.split('\t')
                topics[data[0]] = {}
                topics[data[0]]['weight'] = float(data[1].strip())
    with open(wordweightfile) as f:
        for lines in f:
            line = lines.split('\t')
            if 'data' not in topics[line[0]]:
                topics[line[0]]['data']={}
                for l in labels:
                    topics[line[0]]['data'][l]={}
            for l in labels:
                if line[1] in labels[l]:
                    topics[line[0]]['data'][l][line[1]] = float(line[2].strip())
    for t in topics:
        topics[t]['totalweight']={}
        for l in topics[t]['data']:
            topics[t]['totalweight'][l]=0
            for elt in topics[t]['data'][l]:
                topics[t]['totalweight'][l]+= topics[t]['data'][l][elt]
    items = {}
    for t in topics:
        for l in topics[t]['data']:
            if l not in items:
                items[l]=set()
            items[l] = items[l] | set(topics[t]['data'][l].keys())
    return (topics,items)
​
​
def getTopics():
	phiMatrices = {}
	labels = {}
	labels['concrete'] = pickle.load(open("app/mallet/concrete.p","rb"))
	labels['abstract'] = pickle.load(open("app/mallet/abstract.p","rb"))
	wordweightfile = "app/mallet/topicWordWeight.output"
	keyfile = "app/mallet/icmsdkeys.txt"
	# labels['concrete'] = pickle.load(open(AWS_MALLET_FILES+"concrete.p","rb"))
	# labels['abstract'] = pickle.load(open(AWS_MALLET_FILES+"abstract.p","rb"))
	# wordweightfile = AWS_MALLET_FILES+"topicWordWeight.output"
	# keyfile = AWS_MALLET_FILES+"icmsdkeys.txt"
	(topics,items)= dataPreprocessing(labels, keyfile,wordweightfile)
	# mp = computeMarginalProb(items,topics)
	numTopics = 150
    for jj in topics:
        for l in topics['0']['data']:
            vals = np.array([i/float(topics[jj]['totalweight'][l]) for i in topics[jj]['data'][l].values()])
            try:
                phiMatrices[l]=np.vstack((phiMatrices[l],vals))
            except:
                phiMatrices[l]=vals
    topItemsByTopic = {}
    for t in topics:
        if t not in topItemsByTopic:
            topItemsByTopic[t]={}
        for l in topics['0']['data']:
            res = topics[t]['data'][l]
            sortres = sorted(res.items(),key=operator.itemgetter(1))
            topItemsByTopic[t][l]=[i for i in reversed(sortres[-25:])]
    return (topics, items, phiMatrices, topItemsByTopic)
​
def getItemsByStyle(topics,phiMatrices,AorC):
	inferredTheta = {}
	if AorC == "concrete":
		thetafile = "app/mallet/c2adoctops"
		# thetafile = AWS_MALLET_FILES+"c2adoctops"
	else:
		thetafile = "app/mallet/a2cdoctops"
		# thetafile = AWS_MALLET_FILES+"a2cdoctops"
	with open(thetafile,"r") as f:
		for lines in f:
			data = lines.split('\t')
			try:
				float(data[0])
				if data[1] not in inferredTheta:
	                # print data
					inferredTheta[data[1]] = [float(i.strip()) for i in data[2:]]
	                # print inferredTheta[data[1]]
			except:
				count = 0
	topItemsByStyleWord = {}
	for sty in inferredTheta:
		if AorC == "concrete":
			l = "abstract"
		else:
			l = "concrete"
		topItemsByStyleWord[sty]={}
		#            for lang in phiMatrices:
		rawres = np.dot(inferredTheta[sty],phiMatrices[l])
		itemnames = list(topics['0']['data'][l].keys())
		inds = sorted(range(len(rawres)), key=lambda k: rawres[k])
		tempres = [itemnames[i] for i in reversed(inds[-25:])]
		topItemsByStyleWord[sty]=tempres
	return topItemsByStyleWord