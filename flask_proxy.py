from flask import Flask,render_template,flash,request,redirect,url_for
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
import redis

conRedis = redis.Redis(host='192.168.1.157',port=6379)
# conRedis = redis.Redis(host='127.0.0.1', port=6379)
#应用统称
proxy = Flask(__name__)
proxy.debug = True
proxy.secret_key = '1234as'

class ProxyForm(FlaskForm):
    #第一参数label，是前端显示的名称
    name = StringField('创建新队列:',validators=[DataRequired()])
    submit = SubmitField()

#数据展示
@proxy.route('/proxy/',methods=['GET'])
def showproxy():
    form = ProxyForm()
    quedict = {}
    names = conRedis.smembers('ProxyName')
    if not names:
        flash('IP队列为空')
    for item in names:
        item = item.decode('utf8')
        length = conRedis.llen(item)
        quedict[item] = length
    return render_template('base.html',proxyinfo=quedict,form=form)

'''
删除数据--从ProxyName列表删除名称
'''
@proxy.route('/proxy/del/<name>')
def delproxy(name):
    res = conRedis.srem('ProxyName',name)
    if res:
        flash('{}已经删除'.format(name))
    else:
        flash('{}删除失败'.format(name))
    return redirect(url_for('showproxy'))

'''
队列名，不能有空格。
'''
@proxy.route('/proxy/',methods=['POST'])
def create():
    proxyname = request.form.get('name').strip()
    if proxyname[-6:] != '_proxy':
        flash('创建失败,队列名称要以_proxy结尾')
        return redirect(url_for('showproxy'))
    if proxyname in conRedis.keys():
        flash('{}已经存在'.format(proxyname))
        return redirect(url_for('showproxy'))
    res = conRedis.sadd('ProxyName',proxyname)
    if res:
        flash('{}添加成功'.format(proxyname))
    else:
        flash('{}已经存在'.format(proxyname))
    return redirect(url_for('showproxy'))

if __name__ == '__main__':
    proxy.run(host='10.42.213.125',port=5001)





