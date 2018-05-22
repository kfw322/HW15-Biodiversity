import pandas as pd
import numpy as np
import os
import sqlalchemy
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import matplotlib.pyplot as plt
from flask import Flask, jsonify
import json

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
conn = engine.connect()
Base= automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()
inspector=inspect(engine)
inspector.get_table_names()
inspector.get_columns("samples_metadata")
inspector.get_columns("samples")
inspector.get_columns("otu")

class SamplesMetadata(Base):
    __tablename__ = "samples_metadata"
    __table_args__ = {"extend_existing":True}
    sampleid = Column(Text,primary_key=True)

class Samples(Base):
    __tablename__ = "samples"
    __table_args__ = {"extend_existing":True}
    otu_id = Column(Text,primary_key=True)

class Otu(Base):
    __tablename__ = "otu"
    __table_args__ = {"extend_existing":True}
    otu_id = Column(Text,primary_key=True)

Base.prepare()
session=Session(engine)
app = Flask(__name__)

@app.route("/")
def hw15home():
    return("Sup d00d. welcome to my Homework 15 homepage. Homie. Change this once we have data to put here on this homepage.")

@app.route('/names')
def names():
    samplenamelist = []
    output = session.query(SamplesMetadata)
    for row in output:
        samplenamelist.append("BB_" + str(row.sampleid))
    return(jsonify(samplenamelist))


















if __name__ == "__main__":
    app.run(debug=True)