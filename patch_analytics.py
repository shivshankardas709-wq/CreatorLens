from pathlib import Path
p=Path('app/src/main/java/com/creatorlens/app/MainActivity.java')
s=p.read_text()
s=s.replace('TextView pageTitle, channelName, subValue, viewValue, videoValue, statusText;','TextView pageTitle, channelName, subValue, viewValue, videoValue, statusText;\n    String accessToken;')
s=s.replace('void analytics(){header("Analytics","Your channel performance at a glance");LinearLayout c=card();c.addView(text("Connect YouTube Analytics to unlock historical charts, watch time, CTR and audience metrics.",14,muted));Button b=actionButton("Connect YouTube");c.addView(b,new LinearLayout.LayoutParams(-1,dp(46)));b.setOnClickListener(v->authorizeYouTube());}', '''void analytics(){
        header("Analytics","Real YouTube performance — last 28 days");
        LinearLayout c=card(); TextView info=text("Loading your YouTube Analytics…",14,muted); c.addView(info);
        if(accessToken==null||accessToken.isEmpty()){ Button b=actionButton("Connect YouTube"); c.addView(b,new LinearLayout.LayoutParams(-1,dp(46))); b.setOnClickListener(v->authorizeYouTube()); return; }
        Button refresh=actionButton("Refresh Analytics"); c.addView(refresh,new LinearLayout.LayoutParams(-1,dp(46))); refresh.setOnClickListener(v->fetchAnalytics());
        fetchAnalytics();
    }''')
s=s.replace('if(token==null||token.isEmpty()){toast("No access token returned.");return;}if(statusText!=null)', 'if(token==null||token.isEmpty()){toast("No access token returned.");return;}accessToken=token;if(statusText!=null)')
needle='    void authorizeYouTube(){'
method='''    void fetchAnalytics(){
        if(accessToken==null||accessToken.isEmpty()){toast("Connect YouTube first.");return;}
        new Thread(()->{
            HttpURLConnection c=null;
            try{
                java.text.SimpleDateFormat f=new java.text.SimpleDateFormat("yyyy-MM-dd",java.util.Locale.US);
                java.util.Calendar cal=java.util.Calendar.getInstance();
                String end=f.format(cal.getTime()); cal.add(java.util.Calendar.DAY_OF_YEAR,-27); String start=f.format(cal.getTime());
                String q="https://youtubeanalytics.googleapis.com/v2/reports?ids=channel%3D%3DMINE&startDate="+start+"&endDate="+end+"&metrics=views%2CestimatedMinutesWatched%2CsubscribersGained%2CaverageViewDuration%2CaverageViewPercentage";
                c=(HttpURLConnection)new URL(q).openConnection(); c.setRequestMethod("GET"); c.setRequestProperty("Authorization","Bearer "+accessToken); c.setConnectTimeout(15000); c.setReadTimeout(15000);
                int code=c.getResponseCode(); BufferedReader r=new BufferedReader(new InputStreamReader(code>=200&&code<300?c.getInputStream():c.getErrorStream())); StringBuilder sb=new StringBuilder(); String line; while((line=r.readLine())!=null)sb.append(line); final String body=sb.toString(); final int status=code;
                runOnUiThread(()->{
                    if(status<200||status>=300){toast("Analytics API error: "+status);return;}
                    try{
                        JSONObject ro=new JSONObject(body); JSONArray rows=ro.optJSONArray("rows");
                        if(rows==null||rows.length()==0){toast("No analytics data available for the last 28 days.");return;}
                        JSONArray row=rows.getJSONArray(0);
                        String views=row.optString(0,"0"), minutes=row.optString(1,"0"), gained=row.optString(2,"0"), avg=row.optString(3,"0"), pct=row.optString(4,"0");
                        clear(); header("Analytics","Real YouTube performance — last 28 days");
                        LinearLayout stats=card(); LinearLayout rr=new LinearLayout(this); metric(rr,"VIEWS",formatNumber(views),"Last 28 days"); metric(rr,"WATCH TIME",formatMinutes(minutes),"Minutes watched"); metric(rr,"SUBSCRIBERS","+"+formatNumber(gained),"Subscribers gained"); stats.addView(rr);
                        LinearLayout rr2=new LinearLayout(this); metric(rr2,"AVG VIEW DURATION",formatDuration(avg),"Per view"); metric(rr2,"AVG VIEW %",formatPercent(pct),"Audience retention"); stats.addView(rr2);
                        LinearLayout trend=card(); TextView tt=text("Daily views trend",16,ink);tt.setTypeface(null,1);trend.addView(tt); TextView tv=text("Fetching daily trend…",13,muted);trend.addView(tv); fetchDailyTrend(tv);
                        LinearLayout note=card(); note.addView(text("✓ Data is pulled directly from YouTube Analytics for your connected channel.",13,muted));
                    }catch(Exception e){toast("Analytics response could not be parsed.");}
                });
            }catch(Exception e){runOnUiThread(()->toast("Analytics connection error: "+e.getMessage()));}finally{if(c!=null)c.disconnect();}
        }).start();
    }
    void fetchDailyTrend(TextView target){
        new Thread(()->{HttpURLConnection c=null;try{
            java.text.SimpleDateFormat f=new java.text.SimpleDateFormat("yyyy-MM-dd",java.util.Locale.US);java.util.Calendar cal=java.util.Calendar.getInstance();String end=f.format(cal.getTime());cal.add(java.util.Calendar.DAY_OF_YEAR,-6);String start=f.format(cal.getTime());
            String q="https://youtubeanalytics.googleapis.com/v2/reports?ids=channel%3D%3DMINE&startDate="+start+"&endDate="+end+"&metrics=views&dimensions=day&sort=day";
            c=(HttpURLConnection)new URL(q).openConnection();c.setRequestMethod("GET");c.setRequestProperty("Authorization","Bearer "+accessToken);c.setConnectTimeout(15000);c.setReadTimeout(15000);int code=c.getResponseCode();BufferedReader r=new BufferedReader(new InputStreamReader(code>=200&&code<300?c.getInputStream():c.getErrorStream()));StringBuilder sb=new StringBuilder();String line;while((line=r.readLine())!=null)sb.append(line);final String body=sb.toString();final int status=code;
            runOnUiThread(()->{if(status<200||status>=300){target.setText("Daily trend unavailable (HTTP "+status+").");return;}try{JSONArray rows=new JSONObject(body).optJSONArray("rows");if(rows==null||rows.length()==0){target.setText("No daily trend data available.");return;}StringBuilder out=new StringBuilder();for(int i=0;i<rows.length();i++){JSONArray row=rows.getJSONArray(i);out.append(row.optString(0,""));out.append("   ");out.append(formatNumber(row.optString(1,"0"))).append(" views");if(i<rows.length()-1)out.append("\\n");}target.setText(out.toString());}catch(Exception e){target.setText("Daily trend could not be parsed.");}});
        }catch(Exception e){runOnUiThread(()->target.setText("Daily trend error: "+e.getMessage()));}finally{if(c!=null)c.disconnect();}}).start();
    }
    String formatMinutes(String s){try{long n=(long)Double.parseDouble(s);if(n>=1000)return String.format(java.util.Locale.US,"%.1fK",n/1000.0);return String.valueOf(n);}catch(Exception e){return s;}}
    String formatDuration(String s){try{long sec=(long)Double.parseDouble(s);return (sec/60)+":"+String.format(java.util.Locale.US,"%02d",sec%60);}catch(Exception e){return s+"s";}}
    String formatPercent(String s){try{return String.format(java.util.Locale.US,"%.1f%%",Double.parseDouble(s));}catch(Exception e){return s+"%";}}
'''
s=s.replace(needle,method+needle)
p.write_text(s)
print('Real YouTube Analytics patch upgraded')
