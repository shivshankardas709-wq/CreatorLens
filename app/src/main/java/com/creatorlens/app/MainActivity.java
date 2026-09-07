package com.creatorlens.app;

import android.app.Activity;
import android.content.Intent;
import android.content.IntentSender;
import android.graphics.Color;
import android.os.Bundle;
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
    LinearLayout content; int pad = 18;
    @Override public void onCreate(Bundle b) { super.onCreate(b); build(); }
    TextView tv(String s,int sp){TextView t=new TextView(this);t.setText(s);t.setTextSize(sp);t.setTextColor(Color.rgb(25,27,35));t.setPadding(pad,pad,pad,pad);return t;}
    Button btn(String s){Button b=new Button(this);b.setText(s);b.setAllCaps(false);return b;}
    void build(){LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundColor(Color.rgb(246,247,251));TextView bar=tv("  CreatorLens\n  YouTube Creator Intelligence",20);bar.setTextColor(Color.WHITE);bar.setBackgroundColor(Color.rgb(16,18,26));root.addView(bar,new LinearLayout.LayoutParams(-1,80));LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);String[] ns={"Dashboard","Keywords","Titles","Ideas","Competitors","SEO","Script"};for(String n:ns){Button b=btn(n);b.setOnClickListener(v->show(n));nav.addView(b,new LinearLayout.LayoutParams(0,58,1));}root.addView(nav);content=new LinearLayout(this);content.setOrientation(LinearLayout.VERTICAL);ScrollView sv=new ScrollView(this);sv.addView(content);root.addView(sv,new LinearLayout.LayoutParams(-1,0,1));setContentView(root);show("Dashboard");}
    void show(String n){content.removeAllViews();content.addView(tv(n,28));if(n.equals("Dashboard"))dashboard();else if(n.equals("Keywords"))keywords();else if(n.equals("Titles"))titles();else if(n.equals("Ideas"))ideas();else if(n.equals("Competitors"))competitors();else if(n.equals("SEO"))seo();else script();}
    void card(String s){TextView t=tv(s,16);t.setBackgroundColor(Color.WHITE);content.addView(t,new LinearLayout.LayoutParams(-1,-2));}
    void dashboard(){Button connect=btn("Connect YouTube Channel");content.addView(connect);connect.setOnClickListener(v->authorizeYouTube());card("CHANNEL OVERVIEW\n\nConnect your YouTube account to replace demo numbers with your real channel data.");card("Top Videos\n\nYour real videos will appear here after YouTube authorization.");}
    void authorizeYouTube(){List<Scope> scopes=Arrays.asList(new Scope(YOUTUBE_READONLY),new Scope(YT_ANALYTICS_READONLY));AuthorizationRequest request=AuthorizationRequest.builder().setRequestedScopes(scopes).build();Identity.getAuthorizationClient(this).authorize(request).addOnSuccessListener(result->{if(result.hasResolution()){try{startIntentSenderForResult(result.getPendingIntent().getIntentSender(),AUTH_REQUEST_CODE,null,0,0,0);}catch(IntentSender.SendIntentException e){toast("Could not open Google authorization.");}}else handleAuthorization(result);}).addOnFailureListener(e->toast("Google authorization failed: "+e.getMessage()));}
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(requestCode==AUTH_REQUEST_CODE&&resultCode==RESULT_OK&&data!=null){try{handleAuthorization(Identity.getAuthorizationClient(this).getAuthorizationResultFromIntent(data));}catch(ApiException e){toast("Authorization was not completed.");}}}
    void handleAuthorization(AuthorizationResult result){String token=result.getAccessToken();if(token==null||token.isEmpty()){toast("No access token returned.");return;}card("YouTube Connected\n\nFetching your channel data...");new Thread(()->fetchMyChannel(token)).start();}
    void fetchMyChannel(String token){HttpURLConnection c=null;try{URL u=new URL("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true");c=(HttpURLConnection)u.openConnection();c.setRequestMethod("GET");c.setRequestProperty("Authorization","Bearer "+token);c.setConnectTimeout(15000);c.setReadTimeout(15000);int code=c.getResponseCode();BufferedReader r=new BufferedReader(new InputStreamReader(code>=200&&code<300?c.getInputStream():c.getErrorStream()));StringBuilder sb=new StringBuilder();String line;while((line=r.readLine())!=null)sb.append(line);final String body=sb.toString();final int status=code;runOnUiThread(()->{if(status>=200&&status<300){try{JSONObject ro=new JSONObject(body);JSONArray items=ro.optJSONArray("items");if(items==null||items.length()==0){card("YouTube connected\n\nNo YouTube channel was returned for this Google account.");return;}JSONObject item=items.getJSONObject(0);JSONObject sn=item.optJSONObject("snippet"),st=item.optJSONObject("statistics");String title=sn==null?"Your Channel":sn.optString("title","Your Channel");String subs=st==null?"-":st.optString("subscriberCount","-");String views=st==null?"-":st.optString("viewCount","-");String videos=st==null?"-":st.optString("videoCount","-");card("CHANNEL CONNECTED\n\n"+title+"\n\nSubscribers: "+subs+"\nTotal views: "+views+"\nVideos: "+videos+"\n\nYour real YouTube channel data is connected.");}catch(Exception e){card("YouTube connected\n\nThe channel response could not be parsed.");}}else card("YouTube API error ("+status+")\n\n"+body);});}catch(Exception e){runOnUiThread(()->card("Connection error\n\n"+e.getMessage()));}finally{if(c!=null)c.disconnect();}}
    void input(String hint,String action){EditText e=new EditText(this);e.setHint(hint);content.addView(e);Button b=btn(action);content.addView(b);b.setOnClickListener(v->toast("Demo result generated."));}
    void keywords(){input("e.g. Revelation 9 explained","Research");card("Keyword opportunities\n\nRevelation 9 explained - High demand\nRevelation 9 meaning - Medium competition\nRevelation 9 Bible study - Searchable\nRevelation 9 prophecy - Related");}
    void titles(){input("Enter video topic","Generate Titles");card("AI Title Ideas\n\nThe Terrifying Truth About Your Topic\nYour Topic: What The Bible Really Says\nThe Mystery Finally Explained\nWhat Happens When It Begins?");}
    void ideas(){card("CONTENT IDEAS\n\nThe Mystery Nobody Can Explain\nWhat Really Happened?\n7 Facts You Never Knew\nThe Timeline Explained");}
    void competitors(){input("@channel or channel URL","Analyze");card("Competitor Signals\n\nTopic overlap: 64%\nPosting cadence: 3.2/week\nMedian views: 184K\nGrowth signal: Strong");}
    void seo(){input("Paste your video title","Analyze SEO");card("SEO SCORE\n\n78/100\n\nMain topic detected\nCuriosity signal\nStrengthen searchable phrase\nPut primary keyword earlier");}
    void script(){input("Topic for your video","Create Outline");card("SCRIPT STRUCTURE\n\n1. HOOK - strongest unanswered question.\n2. CONTEXT - only what viewers need.\n3. ESCALATION - reveal evidence in stages.\n4. OPEN LOOP - introduce the biggest mystery.\n5. PAYOFF - deliver the verified conclusion.");}
    void toast(String s){Toast.makeText(this,s,Toast.LENGTH_SHORT).show();}
}
