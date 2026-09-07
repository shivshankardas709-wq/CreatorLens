from pathlib import Path
import re

p=Path('app/src/main/java/com/creatorlens/app/MainActivity.java')
s=p.read_text()
# Modern AndroidX Activity Result API for Google authorization resolution.
s=s.replace('import android.app.Activity;','import android.app.Activity;\nimport androidx.activity.ComponentActivity;\nimport androidx.activity.result.ActivityResultLauncher;\nimport androidx.activity.result.IntentSenderRequest;\nimport androidx.activity.result.contract.ActivityResultContracts;')
s=s.replace('public class MainActivity extends Activity {','public class MainActivity extends ComponentActivity {')
s=re.sub(r'\n\s*ActivityResultLauncher<[^;]+> _unused\d*;', '', s)
s=re.sub(r'\n\s*ActivityResultLauncher<IntentSenderRequest> authorizationLauncher;', '', s)
s=re.sub(r'\n\s*ActivityResultLauncher<androidx\.activity\.result\.ActivityResult> authorizationLauncher;', '', s)
s=s.replace('private static final int AUTH_REQUEST_CODE = 9001;','private static final int AUTH_REQUEST_CODE = 9001;\n    ActivityResultLauncher<IntentSenderRequest> authorizationLauncher;')
old='@Override public void onCreate(Bundle b){super.onCreate(b);buildShell();show("Dashboard");}'
new='''@Override public void onCreate(Bundle b){super.onCreate(b);authorizationLauncher=registerForActivityResult(new ActivityResultContracts.StartIntentSenderForResult(),result->{if(result.getResultCode()!=RESULT_OK){showMessage("Google authorization","Authorization did not complete. Result code: "+result.getResultCode());return;}Intent data=result.getData();if(data==null){showMessage("Google authorization","Google returned no authorization data.");return;}try{handleAuthorization(Identity.getAuthorizationClient(this).getAuthorizationResultFromIntent(data));}catch(ApiException e){showAuthError("Authorization result error",e);}});buildShell();show("Dashboard");}'''
s=s.replace(old,new)
# Replace the old startIntentSenderForResult call and remove its obsolete SendIntentException try/catch wrapper.
s=re.sub(r'try\s*\{\s*authorizationLauncher\.launch\((.*?)\);\s*\}\s*catch\s*\(\s*IntentSender\.SendIntentException\s+e\s*\)\s*\{\s*toast\("Could not open Google authorization\."\);\s*\}', r'authorizationLauncher.launch(\1);', s, flags=re.S)
s=s.replace('startIntentSenderForResult(result.getPendingIntent().getIntentSender(),AUTH_REQUEST_CODE,null,0,0,0);','authorizationLauncher.launch(new IntentSenderRequest.Builder(result.getPendingIntent().getIntentSender()).build());')
s=s.replace('startActivityForResult(result.getPendingIntent().getIntentSender(),AUTH_REQUEST_CODE,null,0,0,0);','authorizationLauncher.launch(new IntentSenderRequest.Builder(result.getPendingIntent().getIntentSender()).build());')
# Also normalize any remaining old try/catch around a direct launcher invocation, regardless of whitespace.
s=re.sub(r'try\s*\{\s*(authorizationLauncher\.launch\([^;]+\);)\s*\}\s*catch\s*\(\s*IntentSender\.SendIntentException\s+e\s*\)\s*\{[^}]*\}', r'\1', s, flags=re.S)
start='    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){'
if start in s:
    a=s.index(start); b=s.find('\n    void handleAuthorization(',a)
    if b!=-1: s=s[:a]+s[b+1:]
p.write_text(s)
print('Fixed ActivityResult launcher compile wrapper; trigger rebuild')
