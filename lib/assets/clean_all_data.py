import os

dirpath = os.getcwd()

os.system('python ' + dirpath + '/lib/assets/clean_notes_data.py')
os.system('python ' + dirpath + '/lib/assets/clean_heart_rate_data.py')
os.system('python ' + dirpath + '/lib/assets/clean_heart_rhythm_data.py')
os.system('python ' + dirpath + '/lib/assets/clean_bp_data.py')
os.system('python ' + dirpath + '/lib/assets/clean_gcs_total_data.py')
os.system('python ' + dirpath + '/lib/assets/clean_platelets_data.py')
os.system('python ' + dirpath + '/lib/assets/clean_creatinine_data.py')
os.system('python ' + dirpath + '/lib/assets/clean_weight_data.py')
