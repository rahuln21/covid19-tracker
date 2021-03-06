from flask import Flask, Markup, render_template
import regress
import scrape
import random
import datetime
app = Flask(__name__)


@app.route('/')
def init():
	stats_list, state_list, confirmed_list, cured_list, death_list = scrape.scrape_now()
	x, y, y_pred, days_pred = regress.final()
	x_actual=[]
	number_of_colors = len(state_list)
	color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
	confirmed_list = [None if v is 0 else v for v in confirmed_list]
	cured_list = [None if v is 0 else v for v in cured_list]
	death_list = [None if v is 0 else v for v in death_list]
	for x_data in x:
		x_actual.append(x_data[0])

	now = datetime.datetime.now()+datetime.timedelta(days=1)
	dates = []
	for i in range(5):
		dates.append(now+datetime.timedelta(days=i))
	
	return render_template('index.html', title='COVID-19 India Tracker', x=x_actual, y=y.tolist(), y_pred=y_pred.tolist(), days_pred=days_pred,
	   color=color, dates=dates, state_list=state_list, stats_list=stats_list, confirmed_list=confirmed_list, cured_list=cured_list, death_list=death_list,total=(int(stats_list[0])+int(stats_list[1])+int(stats_list[2])))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

