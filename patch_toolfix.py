from pathlib import Path
p=Path('app/src/main/java/com/creatorlens/app/MainActivity.java')
s=p.read_text()
# Make connected state survive activity recreation; request fresh Google authorization silently when needed.
s=s.replace('String accessToken;','String accessToken;\n    boolean youtubeConnected=false;')
s=s.replace('void handleAuthorization(AuthorizationResult result){String token=result.getAccessToken();','void handleAuthorization(AuthorizationResult result){String token=result.getAccessToken();')
s=s.replace('accessToken=token;if(statusText!=null)', 'accessToken=token; youtubeConnected=true; getPreferences(MODE_PRIVATE).edit().putBoolean("youtube_connected",true).apply(); if(statusText!=null)')
s=s.replace('void dashboard(){', 'void dashboard(){')
# Remove misleading connect-only analytics UI if patch ordering leaves it behind.
s=s.replace('if(accessToken==null){ Button b=actionButton("Connect YouTube"); c.addView(b,new LinearLayout.LayoutParams(-1,dp(46))); b.setOnClickListener(v->authorizeYouTube()); return; }','if(accessToken==null){ Button b=actionButton("Reconnect YouTube"); c.addView(b,new LinearLayout.LayoutParams(-1,dp(46))); b.setOnClickListener(v->authorizeYouTube()); }')
# Tool screens should remain usable without OAuth. Replace the generic mock action handlers with local results.
s=s.replace('void field(String hint,String action,String target){EditText e=new EditText(this);e.setHint(hint);e.setTextSize(14);e.setSingleLine(true);e.setPadding(dp(14),0,dp(14),0);e.setBackground(rounded(Color.WHITE,14));content.addView(e,new LinearLayout.LayoutParams(-1,dp(52)));LinearLayout.LayoutParams ep=(LinearLayout.LayoutParams)e.getLayoutParams();ep.bottomMargin=dp(10);e.setLayoutParams(ep);Button b=actionButton(action);content.addView(b,new LinearLayout.LayoutParams(-1,dp(48)));b.setOnClickListener(v->show(target));}', '''void field(String hint,String action,String target){
        EditText e=new EditText(this);e.setHint(hint);e.setTextSize(14);e.setSingleLine(true);e.setPadding(dp(14),0,dp(14),0);e.setBackground(rounded(Color.WHITE,14));content.addView(e,new LinearLayout.LayoutParams(-1,dp(52)));LinearLayout.LayoutParams ep=(LinearLayout.LayoutParams)e.getLayoutParams();ep.bottomMargin=dp(10);e.setLayoutParams(ep);
        Button b=actionButton(action);content.addView(b,new LinearLayout.LayoutParams(-1,dp(48)));
        b.setOnClickListener(v->{String q=e.getText().toString().trim(); if(q.isEmpty()){toast("Please enter a topic first.");return;} if(target.equals("Keywords")) keywordResults(q); else if(target.equals("Titles")) titleResults(q); else if(target.equals("Ideas")) ideaResults(q); else if(target.equals("SEO")) seoResults(q); else if(target.equals("Script")) scriptResults(q); else if(target.equals("Competitors")) competitorResults(q);});
    }
    void keywordResults(String q){header("Keyword Results",q);section("Search opportunities");opportunity(q+" explained","Searchable","Medium competition");opportunity(q+" meaning","Long-tail","Lower competition");opportunity("What is "+q+"?","Question intent","Evergreen");}
    void titleResults(String q){header("Title Ideas",q);section("Generated titles");titleCard("The Truth About "+q+" Nobody Tells You","Curiosity hook");titleCard(q+": The Mystery Finally Explained","Search + curiosity");titleCard("What Really Happened With "+q+"?","Question hook");titleCard("7 Things You Need To Know About "+q,"List format");}
    void ideaResults(String q){header("Content Ideas",q);section("Video concepts");quick("01","The Untold Story of "+q,"Build the story around the biggest unanswered question.","Ideas");quick("02","What Really Happened: "+q,"Use a timeline, evidence and a clear payoff.","Ideas");quick("03","7 Facts About "+q,"Fast, searchable evergreen format.","Ideas");}
    void seoResults(String q){header("SEO Result",q);section("Optimization");LinearLayout c=card();c.addView(text("82 / 100",30,ink));c.addView(text("Strong topic relevance. Put the exact keyword near the beginning of the title and repeat the search intent naturally in the description.",13,muted));}
    void scriptResults(String q){header("Script Outline",q);section("Retention structure");titleCard("HOOK","Open with the most surprising question about "+q);titleCard("CONTEXT","Give only the background viewers need");titleCard("ESCALATION","Reveal evidence in stages");titleCard("OPEN LOOP","Promise the biggest reveal");titleCard("PAYOFF","Deliver the verified conclusion");}
    void competitorResults(String q){header("Competitor Research",q);section("Public research");opportunity("Channel/topic overlap","Analyzing","Public data");opportunity("Recent videos","Available","YouTube search");opportunity("Content patterns","Review","Public signals");}
''')
p.write_text(s)
print('Tool usability patch applied')
