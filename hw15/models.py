from .app import db

class SamplesMetadata(db.Model):
    __tablename__ = "samples_metadata"
    __table_args__ = {"extend_existing":True}
    sampleid = db.Column(db.Text,primary_key=True)
    def __repr__(self):
        return '<SamplesMetadata %r>' % (self.sampleid)

class Samples(db.Model):
    __tablename__ = "samples"
    __table_args__ = {"extend_existing":True}
    otu_id = db.Column(db.Text,primary_key=True)
    def __repr__(self):
        return '<Samples %r>' % (self.otu_id)


class Otu(db.Model):
    __tablename__ = "otu"
    __table_args__ = {"extend_existing":True}
    otu_id = db.Column(db.Text,primary_key=True)
    lowest_taxonomic_unit_found = db.Column(db.Text)
    def __repr__(self):
        return '<Otu %r>' % (self.otu_id)
