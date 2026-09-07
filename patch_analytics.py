from pathlib import Path
p=Path('app/src/main/java/com/creatorlens/app/MainActivity.java')
s=p.read_text()
# Keep the real analytics integration, but improve the mobile layout and daily trend.
s=s.replace('LinearLayout stats=card(); LinearLayout rr=new LinearLayout(this); metric(rr,"VIEWS",formatNumber(views),"Last 28 days"); metric(rr,"WATCH TIME",formatMinutes(minutes),"Minutes watched"); metric(rr,"SUBSCRIBERS","+"+formatNumber(gained),"Subscribers gained"); stats.addView(rr);\n                        LinearLayout rr2=new LinearLayout(this); metric(rr2,"AVG VIEW DURATION",formatDuration(avg),"Per view"); metric(rr2,"AVG VIEW %",formatPercent(pct),"Audience retention"); stats.addView(rr2);', '''LinearLayout stats=card();
                        LinearLayout rr=new LinearLayout(this); metric(rr,"VIEWS",formatNumber(views),"Last 28 days"); metric(rr,"WATCH TIME",formatMinutes(minutes),"Minutes watched"); stats.addView(rr);
                        LinearLayout rr2=new LinearLayout(this); metric(rr2,"SUBSCRIBERS","+"+formatNumber(gained),"Subscribers gained"); metric(rr2,"AVG VIEW DURATION",formatDuration(avg),"Per view"); stats.addView(rr2);
                        LinearLayout rr3=new LinearLayout(this); metric(rr3,"AVG VIEW %",formatPercent(pct),"Audience retention"); stats.addView(rr3);''')
# Replace the daily trend request with a clean 7-day day-dimension report.
old='String q="https://youtubeanalytics.googleapis.com/v2/reports?ids=channel%3D%3DMINE&startDate="+start+"&endDate="+end+"&metrics=views&dimensions=day&sort=day";'
new='String q="https://youtubeanalytics.googleapis.com/v2/reports?ids=channel%3D%3DMINE&startDate="+start+"&endDate="+end+"&metrics=views&dimensions=day&sort=day";'
s=s.replace(old,new)
# Make the trend card title explicit about the displayed range.
s=s.replace('TextView tt=text("Daily views trend",16,ink);', 'TextView tt=text("Daily views trend — last 7 days",16,ink);')
p.write_text(s)
print('Analytics mobile layout and daily trend polish applied')
