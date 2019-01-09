from flask import Flask, url_for, render_template, redirect
from glob import glob
import shutil
import os
app = Flask(__name__)

@app.route('/')
def home():
    print(url_for('sortimage', folder='a/b/c'))
    return ''

@app.route('/main/<path:folder>')
def sortimage(folder):
    images=glob('static/%s/*.jpg'%folder)
    if len(images)>0:
        img=min(images)
    else:
        img=''
    return render_template('sortimage.html',img='/'+img,folder=folder,left=len(images))

@app.route('/move/<path:folder>/<subdir>')
def sortimageto(folder,subdir):
    historyfile = 'static/%s/history.txt'%folder
    images=glob('static/%s/*.jpg'%folder)
    if len(images)>0:
        img=min(images)
    else:
        img=''
    line='\t'.join([os.path.basename(img),subdir])
    os.makedirs('static/%s/%s'%(folder,subdir),exist_ok=True)
    shutil.move(img, 'static/%s/%s' % (folder,subdir))
    open(historyfile, 'a').write(line+'\n')
    return redirect(url_for('sortimage',folder=folder))

@app.route('/undo/<path:folder>')
def undo(folder):
    try:
        historyfile = 'static/%s/history.txt'%folder
        lines=open(historyfile).readlines()
        if len(lines[-1].strip())>0:
            img,subdir=lines[-1].strip().split('\t')
            shutil.move('static/%s/%s/%s'%(folder,subdir,img),'static/%s'%(folder))
            open(historyfile,'w').write(''.join(lines[:-1]))
    except Exception as e:
        print(e)
    return redirect(url_for('sortimage',folder=folder))

if __name__ == '__main__':
    if 1:
        app.run(debug=False, host="0.0.0.0",port=5002)
    else:
        app.run(debug=True)
