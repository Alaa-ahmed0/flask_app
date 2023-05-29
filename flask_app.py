from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from flask import Flask, request

def blast(query_sequence, database):
    result_handle = NCBIWWW.qblast("blastn", database, query_sequence)
    blast_record = NCBIXML.read(result_handle)
    hits = []
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            hit = {
                "identity": hsp.identities / hsp.align_length,
                "query_sequence": alignment.title,
                "subject_sequence": hsp.sbjct,
            }
            hits.append(hit)
    return hits
app = Flask(__name__)

@app.route('/blast', methods=['POST'])
def run_blast():
    query_sequence = request.form['query_sequence']
    database = request.form['database']
    hits = blast(query_sequence, database)
    return {"hits": hits}
if __name__ == '__main__':
    app.run(debug=True,port=9000)
import requests

url = "http://localhost:9000/blast"
data = {
    "query_sequence": "ATCG",
    "database": "nt",
}
response = requests.post(url, data=data)
print(response.json())

