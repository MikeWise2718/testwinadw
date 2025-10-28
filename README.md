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