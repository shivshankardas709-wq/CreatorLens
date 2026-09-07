from pathlib import Path
p=Path('app/src/main/java/com/creatorlens/app/MainActivity.java')
s=p.read_text()

# Ensure the connection state fields exist before using them.
if 'boolean youtubeConnected=false;' not in s:
    if 'String accessToken;' in s:
        s=s.replace('String accessToken;', 'String accessToken;\n    boolean youtubeConnected=false;')
    else:
        s=s.replace('TextView pageTitle, channelName, subValue, viewValue, videoValue, statusText;', 'TextView pageTitle, channelName, subValue, viewValue, videoValue, statusText;\n    String accessToken;\n    boolean youtubeConnected=false;')

# Restore the last access token before the first screen is rendered.
old_create='onCreate(Bundle b){super.onCreate(b);buildShell();show("Dashboard");}'
new_create='onCreate(Bundle b){super.onCreate(b);accessToken=getPreferences(MODE_PRIVATE).getString("youtube_access_token",null);youtubeConnected=accessToken!=null&&!accessToken.isEmpty();buildShell();show("Dashboard");}'
if old_create in s:
    s=s.replace(old_create,new_create)

# Save the token whenever Google authorization succeeds.
old_token='accessToken=token; youtubeConnected=true; getPreferences(MODE_PRIVATE).edit().putBoolean("youtube_connected",true).apply();'
new_token='accessToken=token; youtubeConnected=true; getPreferences(MODE_PRIVATE).edit().putBoolean("youtube_connected",true).putString("youtube_access_token",token).apply();'
if old_token in s:
    s=s.replace(old_token,new_token)

# Make Dashboard reflect the persisted connection instead of resetting to "Not connected".
old='LinearLayout connectCard=card();LinearLayout r=new LinearLayout(this);r.setGravity(Gravity.CENTER_VERTICAL);LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);TextView a=text("YouTube channel",12,muted);info.addView(a);channelName=text("Not connected",18,ink);channelName.setTypeface(null,1);info.addView(channelName);r.addView(info,new LinearLayout.LayoutParams(0,-2,1));Button b=actionButton("Connect");r.addView(b,new LinearLayout.LayoutParams(dp(105),dp(46)));connectCard.addView(r);b.setOnClickListener(v->authorizeYouTube());'
new='''LinearLayout connectCard=card();
        LinearLayout r=new LinearLayout(this);r.setGravity(Gravity.CENTER_VERTICAL);LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);
        TextView a=text("YouTube channel",12,muted);info.addView(a);channelName=text(youtubeConnected?"Connected — loading channel…":"Not connected",18,ink);channelName.setTypeface(null,1);info.addView(channelName);
        r.addView(info,new LinearLayout.LayoutParams(0,-2,1));Button b=actionButton(youtubeConnected?"Reconnect":"Connect");r.addView(b,new LinearLayout.LayoutParams(dp(105),dp(46)));connectCard.addView(r);b.setOnClickListener(v->authorizeYouTube());'''
if old in s:
    s=s.replace(old,new)

# Replace dashboard placeholder stats with loading state when a saved connection exists.
old2='subValue=(TextView)((LinearLayout)m1.getChildAt(0)).getChildAt(1);viewValue=(TextView)((LinearLayout)m1.getChildAt(1)).getChildAt(1);videoValue=(TextView)((LinearLayout)m1.getChildAt(2)).getChildAt(1);'
new2='''subValue=(TextView)((LinearLayout)m1.getChildAt(0)).getChildAt(1);viewValue=(TextView)((LinearLayout)m1.getChildAt(1)).getChildAt(1);videoValue=(TextView)((LinearLayout)m1.getChildAt(2)).getChildAt(1);
        if(youtubeConnected){subValue.setText("Loading…");viewValue.setText("Loading…");videoValue.setText("Loading…");}'''
if old2 in s:
    s=s.replace(old2,new2)

# Make the dashboard chart/status text reflect the connection.
s=s.replace('TextView cp=text("Your performance chart will appear here after Analytics access is connected.",13,muted);', 'TextView cp=text(youtubeConnected?"Live channel data is connected. Analytics charts are available below.":"Connect YouTube to load your live channel performance.",13,muted);')
s=s.replace('statusText=text("YouTube is not connected yet.",13,muted);st.addView(statusText);', 'statusText=text(youtubeConnected?"✓ YouTube connected — your channel data will load automatically.":"YouTube is not connected yet.",13,muted);st.addView(statusText);if(youtubeConnected)new Thread(()->fetchMyChannel(accessToken)).start();')

# If an expired token is rejected, clear the saved connection so the user can reconnect.
s=s.replace('else showMessage("YouTube API error","HTTP "+status+"\\n\\n"+extractApiError(body));', 'else { if(status==401){ accessToken=null; youtubeConnected=false; getPreferences(MODE_PRIVATE).edit().remove("youtube_access_token").putBoolean("youtube_connected",false).apply(); } showMessage("YouTube API error","HTTP "+status+"\\n\\n"+extractApiError(body)); }')

p.write_text(s)
print('YouTube connection persistence patch applied')
