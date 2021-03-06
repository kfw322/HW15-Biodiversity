from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request, redirect, flash
import pandas as pd
import numpy as np
import os
import sqlalchemy
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float
from sqlalchemy.sql import text
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base
import json


engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
Base= automap_base()
Base.prepare(engine,reflect=True)
Otu = Base.classes.otu
Samples = Base.classes.samples
SamplesMetadata= Base.classes.samples_metadata
s=sessionmaker(bind=engine)
session=scoped_session(s)

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///belly_button_biodiversity.sqlite?check_same_thread=False"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#from .models import SamplesMetadata, Samples, Otu

# class SamplesMetadata(Base):
#     __tablename__ = "samples_metadata"
#     __table_args__ = {"extend_existing":True}
#     sampleid = Column(Text,primary_key=True)

# class Samples(Base):
#     __tablename__ = "samples"
#     __table_args__ = {"extend_existing":True}
#     otu_id = Column(Text,primary_key=True)

# class Otu(Base):
#     __tablename__ = "otu"
#     __table_args__ = {"extend_existing":True}
#     otu_id = Column(Text,primary_key=True)

@app.route("/")
def hw15home():
    return render_template("index.html")

@app.route('/names')
def names():
    samplenamelist = []
    output = session.query(SamplesMetadata)
    for row in output:
        samplenamelist.append("BB_" + str(row.SAMPLEID))
    return(jsonify(samplenamelist))

@app.route("/otu")
def otu():
    otudesclist = []
    output = session.query(Otu)
    for row in output:
        otudesclist.append(str(row.lowest_taxonomic_unit_found))
    return(jsonify(otudesclist))

@app.route("/metadata/<sample>")
def metadata(sample):
    data_dict = {}
    output = session.query(SamplesMetadata).filter(SamplesMetadata.SAMPLEID==sample.lower().replace("bb_",""))
    for row in output:
        data_dict["age"]=row.AGE
        data_dict["bbtype"]=row.BBTYPE
        data_dict["ethnicity"]=row.ETHNICITY
        data_dict["gender"]=row.GENDER
        data_dict["location"]=row.LOCATION
        data_dict["sampleid"]=row.SAMPLEID
    return(jsonify(data_dict))

@app.route("/wfreq/<sample>")
def wash(sample):
    output = session.query(SamplesMetadata).filter(SamplesMetadata.SAMPLEID==sample.lower().replace("bb_",""))
    for row in output:
        wash_freq = row.WFREQ
    return(jsonify(int(wash_freq)))

@app.route('/samples/<sample>')
def samples(sample):
    otu_ids = []
    sample_values = []
    c = engine.connect()
    output = c.execute(text(f"select otu_id, {sample} from samples order by {sample} desc"))
    for row in output:
        otu_ids.append(str(row[0]))
        sample_values.append(str(row[1]))
    sample_data = {}
    sample_data["otu_ids"] = otu_ids
    sample_data["sample_values"] = sample_values
    list_of_sample_data_dicts = []
    list_of_sample_data_dicts.append(sample_data)
    return(jsonify(list_of_sample_data_dicts))

if __name__ == "__main__":
    app.run(debug=True)