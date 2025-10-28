# Test ADW
- THis script is for testing deployment on ADW
- It is based from scripts and code extracted from Tac06 
   - did Tac07 by mistake at first, reverted to Tac06
   - `.claude` directory (including commands and settings)
   - `adws` directory (python scripts driving top level loop)
   - `scripts` directory
- It is synced with a github repo by the sane mane
- In its current form it only works with the ANthropic API key, so not with a Calude Max subscription
- The key is read out of the environment, it is not present in the repo
- To test enter an issue and make sure it can be classified by the workflow
- run `uv safasdf` 

# To use it
  -  Run the monitoring script
      - `cd adws\adw_triggers`
      - `uv run trigger_cron.py`
  -  It will automatically process:
     - New issues with no comments
     - Issues where latest comment is "adw"
     
     
# Changes to make windows work
- Windows use an different codepage by delete cp1254 or something.
- utils.py -  line 47   file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
- github.py - line 99 - result = subprocess.run(cmd, capture_output=True, text=True, env=env, encoding='utf-8')
- utils.py - added windows environmental variables
added these lines:
```
        # Windows-specific environment variables (needed for DLL loading)
        "SYSTEMROOT": os.getenv("SYSTEMROOT"),
        "WINDIR": os.getenv("WINDIR"),
        "TEMP": os.getenv("TEMP"),
        "TMP": os.getenv("TMP"),
        "PATHEXT": os.getenv("PATHEXT"),
        "COMSPEC": os.getenv("COMSPEC"),   
        
         # Windows user profile variables (needed for config/cache access)
         "USERPROFILE": os.getenv("USERPROFILE"),
         "USERNAME": os.getenv("USERNAME"),
         "HOMEDRIVE": os.getenv("HOMEDRIVE"),
         "HOMEPATH": os.getenv("HOMEPATH"),
         "APPDATA": os.getenv("APPDATA"),
         "LOCALAPPDATA": os.getenv("LOCALAPPDATA"),                     
```
- API key was broken somehow by copy and pasting
- agents.py - don't think any changes were necessary, but made a lot of debugging changes, so not sure
