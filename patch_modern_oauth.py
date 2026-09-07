from pathlib import Path
p=Path('app/src/main/java/com/creatorlens/app/MainActivity.java')
s=p.read_text()
# Modern AndroidX Activity Result API for Google authorization resolution.
s=s.replace('import android.app.Activity;','import android.app.Activity;\nimport androidx.activity.ComponentActivity;\nimport androidx.activity.result.ActivityResultLauncher;\nimport androidx.activity.result.IntentSenderRequest;\nimport androidx.activity.result.contract.ActivityResultContracts;')
s=s.replace('public class MainActivity extends Activity {','public class MainActivity extends ComponentActivity {')
# Remove any stale launcher declarations from earlier experimental patches.
import re
s=re.sub(r'\n\s*ActivityResultLauncher<[^;]+> _unused\d*;', '', s)
s=re.sub(r'\n\s*ActivityResultLauncher<IntentSenderRequest> authorizationLauncher;', '', s)
s=re.sub(r'\n\s*ActivityResultLauncher<androidx\.activity\.result\.ActivityResult> authorizationLauncher;', '', s)
# One correctly typed launcher.
s=s.replace('private static final int AUTH_REQUEST_CODE = 9001;','private static final int AUTH_REQUEST_CODE = 9001;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> authorizationLauncher;')
old='@Override public void onCreate(Bundle b){super.onCreate(b);buildShell();show("Dashboard");}'
new='''@Override public void onCreate(Bundle b){super.onCreate(b);authorizationLauncher=registerForActivityResult(new ActivityResultContracts.StartIntentSenderForResult(),result->{if(result.getResultCode()!=RESULT_OK){showMessage("Google authorization","Authorization did not complete. Result code: "+result.getResultCode());return;}Intent data=result.getData();if(data==null){showMessage("Google authorization","Google returned no authorization data.");return;}try{handleAuthorization(Identity.getAuthorizationClient(this).getAuthorizationResultFromIntent(data));}catch(ApiException e){showAuthError("Authorization result error",e);}});buildShell();show("Dashboard");}'''
s=s.replace(old,new)
# Support either legacy startIntentSenderForResult spelling from previous patches.
s=s.replace('startIntentSenderForResult(result.getPendingIntent().getIntentSender(),AUTH_REQUEST_CODE,null,0,0,0);','authorizationLauncher.launch(new IntentSenderRequest.Builder(result.getPendingIntent().getIntentSender()).build());')
s=s.replace('startActivityForResult(result.getPendingIntent().getIntentSender(),AUTH_REQUEST_CODE,null,0,0,0);','authorizationLauncher.launch(new IntentSenderRequest.Builder(result.getPendingIntent().getIntentSender()).build());')
# Remove legacy callback if present.
start='    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){'
if start in s:
    a=s.index(start); b=s.find('\n    void handleAuthorization(',a)
    if b!=-1: s=s[:a]+s[b+1:]
p.write_text(s)
print('Applied modern AndroidX Activity Result OAuth flow')
