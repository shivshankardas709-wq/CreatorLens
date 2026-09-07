from pathlib import Path
p=Path('app/src/main/java/com/creatorlens/app/MainActivity.java')
s=p.read_text()
# Modern Activity Result API for Google authorization resolution.
s=s.replace('import android.app.Activity;\n', 'import android.app.Activity;\nimport androidx.activity.result.ActivityResultLauncher;\nimport androidx.activity.result.IntentSenderRequest;\nimport androidx.activity.result.contract.ActivityResultContracts;\n')
s=s.replace('LinearLayout content;', 'ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused2;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused3;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused4;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused5;\n    ActivityResultLauncher<Intent> _unused6;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused7;\n    ActivityResultLauncher<IntentSenderRequest> authorizationLauncher;\n    LinearLayout content;')
# Remove accidental placeholder fields by keeping only the actual launcher.
s=s.replace('    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused2;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused3;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused4;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused5;\n    ActivityResultLauncher<Intent> _unused6;\n    ActivityResultLauncher<androidx.activity.result.ActivityResult> _unused7;\n','')
old='@Override public void onCreate(Bundle b){super.onCreate(b);buildShell();show("Dashboard");}'
new='''@Override public void onCreate(Bundle b){super.onCreate(b);authorizationLauncher=registerForActivityResult(new ActivityResultContracts.StartIntentSenderForResult(),result->{if(result.getResultCode()!=RESULT_OK){showMessage("Google authorization","Authorization did not complete. Result code: "+result.getResultCode());return;}Intent data=result.getData();if(data==null){showMessage("Google authorization","Google returned no authorization data.");return;}try{handleAuthorization(Identity.getAuthorizationClient(this).getAuthorizationResultFromIntent(data));}catch(ApiException e){showAuthError("Authorization result error",e);}});buildShell();show("Dashboard");}'''
s=s.replace(old,new)
old2='startActivityForResult(result.getPendingIntent().getIntentSender(),AUTH_REQUEST_CODE,null,0,0,0);'
new2='authorizationLauncher.launch(new IntentSenderRequest.Builder(result.getPendingIntent().getIntentSender()).build());'
s=s.replace(old2,new2)
# If the old callback remains, neutralize it so the launcher is the single result path.
old3='@Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(requestCode==AUTH_REQUEST_CODE){if(resultCode!=RESULT_OK){showMessage("Google authorization","Authorization did not complete. Result code: "+resultCode);return;}if(data==null){showMessage("Google authorization","Google returned no authorization data.");return;}try{handleAuthorization(Identity.getAuthorizationClient(this).getAuthorizationResultFromIntent(data));}catch(ApiException e){showAuthError("Authorization result error",e);}}}'
s=s.replace(old3,'')
p.write_text(s)
print('Applied modern Activity Result OAuth flow')
