package com.creatorlens.app;

import android.app.Activity;
import android.content.Intent;
import android.content.IntentSender;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.*;
import com.google.android.gms.auth.api.identity.AuthorizationRequest;
import com.google.android.gms.auth.api.identity.AuthorizationResult;
import com.google.android.gms.auth.api.identity.Identity;
import com.google.android.gms.common.api.ApiException;
import com.google.android.gms.common.api.Scope;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Arrays;
import java.util.List;
import org.json.JSONArray;
import org.json.JSONObject;

public class MainActivity extends Activity {
    private static final int AUTH_REQUEST_CODE = 9001;
    private static final String YOUTUBE_READONLY = "https://www.googleapis.com/auth/youtube.readonly";
    private static final String YT_ANALYTICS_READONLY = "https://www.googleapis.com/auth/yt-analytics.readonly";
    LinearLayout content;
    TextView pageTitle, channelName, subValue, viewValue, videoValue, statusText;
    int ink = Color.rgb(24, 27, 38), muted = Color.rgb(104, 111, 130), bg = Color.rgb(246, 247, 251), accent = Color.rgb(102, 76, 245);
    int dp(float n){return (int)(n*getResources().getDisplayMetrics().density+0.5f);}
    TextView text(String s,float size,int color){TextView t=new TextView(this);t.setText(s);t.setTextSize(size);t.setTextColor(color);t.setFontFeatureSettings("kern");return t;}
    GradientDrawable rounded(int color,float radius){GradientDrawable g=new GradientDrawable();g.setColor(color);g.setCornerRadius(dp(radius));return g;}
    TextView pill(String s){TextView t=text(s,12,accent);t.setGravity(Gravity.CENTER);t.setPadding(dp(12),dp(6),dp(12),dp(6));t.setBackground(rounded(Color.rgb(238,234,255),40));return t;}
    Button actionButton(String s){Button b=new Button(this);b.setText(s);b.setTextSize(14);b.setTextColor(Color.WHITE);b.setAllCaps(false);b.setGravity(Gravity.CENTER);b.setBackground(rounded(accent,18));b.setPadding(dp(8),0,dp(8),0);return b;}
    @Override public void onCreate(Bundle b){super.onCreate(b);buildShell();show("Dashboard");}
    void buildShell(){
        LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundColor(bg);
        LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);top.setPadding(dp(20),dp(12),dp(20),dp(12));top.setBackgroundColor(Color.WHITE);
        TextView logo=text("C",22,Color.WHITE);logo.setGravity(Gravity.CENTER);logo.setBackground(rounded(accent,14));top.addView(logo,new LinearLayout.LayoutParams(dp(42),dp(42)));
        LinearLayout brand=new LinearLayout(this);brand.setOrientation(LinearLayout.VERTICAL);brand.setPadding(dp(12),0,0,0);TextView bn=text("CreatorLens",20,ink);bn.setTypeface(null,1);brand.addView(bn);brand.addView(text("Creator intelligence",11,muted));top.addView(brand,new LinearLayout.LayoutParams(0,-2,1));
        TextView notif=text("•••",22,muted);notif.setGravity(Gravity.CENTER);top.addView(notif,new LinearLayout.LayoutParams(dp(42),dp(42)));
        root.addView(top,new LinearLayout.LayoutParams(-1,dp(70)));
        ScrollView sv=new ScrollView(this);content=new LinearLayout(this);content.setOrientation(LinearLayout.VERTICAL);content.setPadding(dp(18),dp(18),dp(18),dp(28));sv.addView(content);root.addView(sv,new LinearLayout.LayoutParams(-1,0,1));
        LinearLayout nav=new LinearLayout(this);nav.setPadding(dp(6),dp(8),dp(6),dp(8));nav.setGravity(Gravity.CENTER);nav.setBackgroundColor(Color.WHITE);
        String[][] ns={{"⌂","Home"},{"⌕","Research"},{"✦","AI Tools"},{"☷","Analytics"}};
        for(String[] n:ns){LinearLayout item=new LinearLayout(this);item.setOrientation(LinearLayout.VERTICAL);item.setGravity(Gravity.CENTER);TextView ic=text(n[0],22,muted);ic.setGravity(Gravity.CENTER);item.addView(ic,new LinearLayout.LayoutParams(-1,dp(28)));TextView lab=text(n[1],10,muted);lab.setGravity(Gravity.CENTER);item.addView(lab);item.setOnClickListener(v->{if(n[1].equals("Home"))show("Dashboard");else if(n[1].equals("Research"))show("Keywords");else if(n[1].equals("AI Tools"))show("Titles");else show("Analytics");});nav.addView(item,new LinearLayout.LayoutParams(0,dp(58),1));}
        root.addView(nav,new LinearLayout.LayoutParams(-1,dp(74)));setContentView(root);
    }
    void clear(){content.removeAllViews();}
    void header(String title,String sub){pageTitle=text(title,28,ink);pageTitle.setTypeface(null,1);content.addView(pageTitle);TextView s=text(sub,13,muted);s.setPadding(0,dp(5),0,dp(18));content.addView(s);}
    TextView section(String s){TextView t=text(s.toUpperCase(),12,muted);t.setTypeface(null,1);t.setPadding(0,dp(20),0,dp(10));content.addView(t);return t;}
    LinearLayout card(){LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(16),dp(16),dp(16),dp(16));c.setBackground(rounded(Color.WHITE,18));content.addView(c,new LinearLayout.LayoutParams(-1,-2));LinearLayout.LayoutParams p=(LinearLayout.LayoutParams)c.getLayoutParams();p.bottomMargin=dp(12);c.setLayoutParams(p);return c;}
    void metric(LinearLayout parent,String label,String value,String delta){LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.VERTICAL);TextView l=text(label,11,muted);row.addView(l);TextView v=text(value,22,ink);v.setTypeface(null,1);v.setPadding(0,dp(4),0,dp(2));row.addView(v);TextView d=text(delta,11,Color.rgb(25,150,93));row.addView(d);parent.addView(row,new LinearLayout.LayoutParams(0,-2,1));}
    void show(String n){clear();if(n.equals("Dashboard"))dashboard();else if(n.equals("Keywords"))keywords();else if(n.equals("Titles"))titles();else if(n.equals("Ideas"))ideas();else if(n.equals("Competitors"))competitors();else if(n.equals("SEO"))seo();else if(n.equals("Analytics"))analytics();else script();}
    void dashboard(){
        header("Good to see you 👋","Your YouTube command center");
        LinearLayout connectCard=card();LinearLayout r=new LinearLayout(this);r.setGravity(Gravity.CENTER_VERTICAL);LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);TextView a=text("YouTube channel",12,muted);info.addView(a);channelName=text("Not connected",18,ink);channelName.setTypeface(null,1);info.addView(channelName);r.addView(info,new LinearLayout.LayoutParams(0,-2,1));Button b=actionButton("Connect");r.addView(b,new LinearLayout.LayoutParams(dp(105),dp(46)));connectCard.addView(r);b.setOnClickListener(v->authorizeYouTube());
        section("Channel performance");LinearLayout stats=card();LinearLayout m1=new LinearLayout(this);metric(m1,"SUBSCRIBERS","—","Connect YouTube");metric(m1,"TOTAL VIEWS","—","Connect YouTube");metric(m1,"VIDEOS","—","Connect YouTube");stats.addView(m1);
        subValue=(TextView)((LinearLayout)m1.getChildAt(0)).getChildAt(1);viewValue=(TextView)((LinearLayout)m1.getChildAt(1)).getChildAt(1);videoValue=(TextView)((LinearLayout)m1.getChildAt(2)).getChildAt(1);
        LinearLayout chart=card();TextView ct=text("Views & subscriber growth",16,ink);ct.setTypeface(null,1);chart.addView(ct);TextView cp=text("Your performance chart will appear here after Analytics access is connected.",13,muted);cp.setPadding(0,dp(8),0,dp(4));chart.addView(cp);Space sp=new Space(this);chart.addView(sp,new LinearLayout.LayoutParams(-1,dp(70)));
        section("Quick tools");quick("🔎","Keyword Research","Find searchable topics with demand and competition.","Keywords");quick("✦","AI Title Generator","Turn any topic into stronger clickable titles.","Titles");quick("💡","Content Ideas","Discover your next videos before you run out of ideas.","Ideas");
        section("Connection status");LinearLayout st=card();statusText=text("YouTube is not connected yet.",13,muted);st.addView(statusText);
    }
    void quick(String icon,String title,String desc,String target){LinearLayout c=card();LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER_VERTICAL);TextView i=text(icon,25,ink);i.setGravity(Gravity.CENTER);row.addView(i,new LinearLayout.LayoutParams(dp(45),dp(45)));LinearLayout inf=new LinearLayout(this);inf.setOrientation(LinearLayout.VERTICAL);inf.setPadding(dp(10),0,0,0);TextView t=text(title,16,ink);t.setTypeface(null,1);inf.addView(t);TextView d=text(desc,12,muted);d.setPadding(0,dp(4),0,0);inf.addView(d);row.addView(inf,new LinearLayout.LayoutParams(0,-2,1));c.addView(row);c.setOnClickListener(v->show(target));}
    void field(String hint,String action,String target){EditText e=new EditText(this);e.setHint(hint);e.setTextSize(14);e.setSingleLine(true);e.setPadding(dp(14),0,dp(14),0);e.setBackground(rounded(Color.WHITE,14));content.addView(e,new LinearLayout.LayoutParams(-1,dp(52)));LinearLayout.LayoutParams ep=(LinearLayout.LayoutParams)e.getLayoutParams();ep.bottomMargin=dp(10);e.setLayoutParams(ep);Button b=actionButton(action);content.addView(b,new LinearLayout.LayoutParams(-1,dp(48)));b.setOnClickListener(v->show(target));}
    void keywords(){header("Keyword Research","Find topics worth making videos about");field("e.g. Revelation 9 explained","Research Keywords","Keywords");section("Opportunity examples");opportunity("Revelation 9 explained","High demand","Medium competition");opportunity("Revelation 9 meaning","Strong search","Medium competition");opportunity("Bible prophecy explained","Evergreen","High competition");}
    void opportunity(String key,String demand,String comp){LinearLayout c=card();TextView t=text(key,16,ink);t.setTypeface(null,1);c.addView(t);LinearLayout r=new LinearLayout(this);r.setPadding(0,dp(10),0,0);r.addView(pill(demand));Space sp=new Space(this);r.addView(sp,new LinearLayout.LayoutParams(dp(8),1));r.addView(pill(comp));c.addView(r);}
    void titles(){header("AI Title Generator","Create clickable titles without losing search intent");field("Enter your video topic","Generate Titles","Titles");section("Sample title set");titleCard("The Terrifying Truth About Your Topic","Curiosity + emotional hook");titleCard("Your Topic: What You Were Never Told","Curiosity gap");titleCard("The Mystery Finally Explained","Simple + searchable");}
    void titleCard(String s,String tag){LinearLayout c=card();TextView t=text(s,16,ink);t.setTypeface(null,1);c.addView(t);c.addView(pill(tag));}
    void ideas(){header("Content Ideas","Build a pipeline of videos around your niche");section("Recommended next videos");quick("01","The Mystery Nobody Can Explain","Open with the strongest unanswered question.","Ideas");quick("02","What Really Happened?","Use evidence, timeline and a clear payoff.","Ideas");quick("03","7 Facts You Never Knew","Great format for searchable evergreen topics.","Ideas");}
    void competitors(){header("Competitor Research","Understand public signals from other channels");field("@channel or YouTube channel URL","Analyze Channel","Competitors");section("Public signals");opportunity("Topic overlap","64%","Strong");opportunity("Posting cadence","3.2 / week","Consistent");opportunity("Median views","184K","Public estimate");}
    void seo(){header("SEO Analyzer","Improve search relevance and viewer intent");field("Paste your video title","Analyze SEO","SEO");section("Score preview");LinearLayout c=card();TextView score=text("78 / 100",30,ink);score.setTypeface(null,1);c.addView(score);c.addView(text("Good foundation. Put the primary keyword earlier and strengthen the curiosity signal.",13,muted));}
    void script(){header("AI Script Assistant","Turn a topic into a retention-focused structure");field("Topic for your video","Create Outline","Script");section("Structure");titleCard("1. HOOK","Strong unanswered question");titleCard("2. CONTEXT","Only what viewers need");titleCard("3. ESCALATION","Reveal evidence in stages");titleCard("4. OPEN LOOP","Introduce the biggest mystery");titleCard("5. PAYOFF","Deliver the verified conclusion");}
    void analytics(){header("Analytics","Your channel performance at a glance");LinearLayout c=card();c.addView(text("Connect YouTube Analytics to unlock historical charts, watch time, CTR and audience metrics.",14,muted));Button b=actionButton("Connect YouTube");c.addView(b,new LinearLayout.LayoutParams(-1,dp(46)));b.setOnClickListener(v->authorizeYouTube());}
    void authorizeYouTube(){List<Scope> scopes=Arrays.asList(new Scope(YOUTUBE_READONLY),new Scope(YT_ANALYTICS_READONLY));AuthorizationRequest req=AuthorizationRequest.builder().setRequestedScopes(scopes).build();Identity.getAuthorizationClient(this).authorize(req).addOnSuccessListener(result->{if(result.hasResolution()){try{startIntentSenderForResult(result.getPendingIntent().getIntentSender(),AUTH_REQUEST_CODE,null,0,0,0);}catch(IntentSender.SendIntentException e){toast("Could not open Google authorization.");}}else handleAuthorization(result);}).addOnFailureListener(e->toast("Google authorization failed: "+e.getMessage()));}
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(requestCode==AUTH_REQUEST_CODE&&resultCode==RESULT_OK&&data!=null){try{handleAuthorization(Identity.getAuthorizationClient(this).getAuthorizationResultFromIntent(data));}catch(ApiException e){toast("Authorization was not completed.");}}}
    void handleAuthorization(AuthorizationResult result){String token=result.getAccessToken();if(token==null||token.isEmpty()){toast("No access token returned.");return;}if(statusText!=null)statusText.setText("Connected — fetching your channel data…");new Thread(()->fetchMyChannel(token)).start();}
    void fetchMyChannel(String token){HttpURLConnection c=null;try{URL u=new URL("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true");c=(HttpURLConnection)u.openConnection();c.setRequestMethod("GET");c.setRequestProperty("Authorization","Bearer "+token);c.setConnectTimeout(15000);c.setReadTimeout(15000);int code=c.getResponseCode();BufferedReader r=new BufferedReader(new InputStreamReader(code>=200&&code<300?c.getInputStream():c.getErrorStream()));StringBuilder sb=new StringBuilder();String line;while((line=r.readLine())!=null)sb.append(line);final String body=sb.toString();final int status=code;runOnUiThread(()->{if(status>=200&&status<300){try{JSONObject ro=new JSONObject(body);JSONArray items=ro.optJSONArray("items");if(items==null||items.length()==0){toast("No YouTube channel found.");return;}JSONObject item=items.getJSONObject(0);JSONObject sn=item.optJSONObject("snippet"),st=item.optJSONObject("statistics");String title=sn==null?"Your Channel":sn.optString("title","Your Channel");String subs=st==null?"-":st.optString("subscriberCount","-");String views=st==null?"-":st.optString("viewCount","-");String videos=st==null?"-":st.optString("videoCount","-");if(channelName!=null)channelName.setText(title);if(subValue!=null)subValue.setText(formatNumber(subs));if(viewValue!=null)viewValue.setText(formatNumber(views));if(videoValue!=null)videoValue.setText(formatNumber(videos));if(statusText!=null)statusText.setText("✓ YouTube connected successfully");}catch(Exception e){toast("Channel response could not be parsed.");}}else toast("YouTube API error: "+status);});}catch(Exception e){runOnUiThread(()->toast("Connection error: "+e.getMessage()));}finally{if(c!=null)c.disconnect();}}
    String formatNumber(String s){try{long n=Long.parseLong(s);if(n>=1000000)return String.format("%.1fM",n/1000000.0);if(n>=1000)return String.format("%.1fK",n/1000.0);return s;}catch(Exception e){return s;}}
    void toast(String s){Toast.makeText(this,s,Toast.LENGTH_LONG).show();}
}
