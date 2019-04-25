require 'csv'
require 'yaml'



class HomeController < ApplicationController
  def index
  flash[:success] = nil
  end
  
  def results
    flash.clear
    flash[:success] = "Successful Predictive Analysis"

    table = CSV.read("#{Rails.root}/uploads/Patient Data.csv", headers: true)
    time = table['charttime']
    hr = table['heart_rate']
    bp = table['abp_systolic']
    pl = table['platelets']
    cr = table['creatinine']
    
    @HR_series_data = [time, hr].transpose
    @HR_series_a =  [time, Array.new(time.length, 100)].transpose
    @HR_series_b =  [time, Array.new(time.length, 60)].transpose
    
    @SBP_series_data = [time, bp].transpose
    @SBP_series_a =  [time, Array.new(time.length, 110)].transpose
    @SBP_series_b =  [time, Array.new(time.length, 130)].transpose
    @SBP_series_c =  [time, Array.new(time.length, 180)].transpose
    
    @Platelet_series_data = [time, pl].transpose
    @Platelet_series_a =  [time, Array.new(time.length, 150)].transpose
    
    @Creatinine_series_data = [time, cr].transpose
    
    # data fill for patient and model info
    
    @patient_risk = session[:L2_score].to_i
    
    @patient_risk_str = @patient_risk.to_s + '%'
    @patient_ID = ((table['subject_id']).first).to_s
    @patient_DOB = ((table['dob']).first).to_s
    @patient_arrive_time = ((table['admittime']).first).to_s
    @patient_age = 10# @patient_arrive_time.match(/.*\/.*\/(\d*)/).captures.to_s[2..5].to_i -  @patient_DOB.match(/.*\/.*\/(\d*)/).captures.to_s[2..5].to_i
    @patient_ICU_time = ((table['intime']).first).to_s
    @patient_gender = ((table['gender']).first).to_s
    @patient_ethnicity = ((table['ethnicity']).first).to_s
    
    @model_DNN_score = session[:DNN_score]
    @model_DNN_auroc = session[:DNN_auroc]
    @model_L1_score = session[:L1_score]
    @model_L1_auroc = session[:L1_auroc]
    @model_L2_score = session[:L2_score]
    @model_L2_auroc = session[:L2_auroc]
    
    @image_patient_risk = round_to_next_5(@patient_risk)
    @image_path = '/assets/risk_' + @image_patient_risk.to_s + '.jpg'
    
    @doctor_notes = session[:doctor_notes];
    @event_notes = session[:event_notes];
    @discharge_notes = session[:discharge_notes];
  end
  
  def create
    session[:id] = 0
    flash.clear
    
    if !params.has_key? (:user_input)
      flash[:alert] = "Please Input a CSV File"
      redirect_to '/analysis'
    else
      #Uploads the CSV into the /uploads directory
      uploaded_io = params[:user_input][:data]
      
      # Validate the file format, redirect if not a CSV
      if uploaded_io.content_type != "application/octet-stream"
        flash[:alert] = "Incorrect File Type"
        redirect_to '/analysis'
      end
      
      #Save the file and move on
      File.open(Rails.root.join('uploads', 'Patient Data.csv'), 'wb') do |file|
        file.write(uploaded_io.read)
        
        #Go and save our notes into the session variable
        @python_notes = `python lib/assets/return_notes.py`;
        @python_notes = YAML.load(@python_notes)

        session[:doctor_notes] =  @python_notes[0];
        session[:event_notes] =  @python_notes[1];
        session[:discharge_notes] =  @python_notes[2];

        #Run our cleaning scripts on the file
        @python_clean_data = "python lib/assets/clean_all_data.py";
        @python_return = `#{@python_clean_data}`;
         
        #Call the Fancy Python Script
        @python_model_connect = "python3 lib/assets/make_connection.py";
        @python_model_return = `#{@python_model_connect}`.split(',');

        session[:DNN_score] = ((@python_model_return[0].gsub("'", "").gsub("[", "")).to_f * 100).round(2)
        session[:L1_score] = ((@python_model_return[1].gsub("'", "")).to_f * 100).round(2)
        session[:L2_score] = ((@python_model_return[2].gsub("'", "")).to_f * 100).round(2)
        session[:DNN_auroc] = @python_model_return[3].to_f.round(2)
        session[:L1_auroc] = @python_model_return[4].to_f.round(2)
        session[:L2_auroc] = @python_model_return[5].gsub("]", "").to_f.round(2)
        
        redirect_to '/results'
      end
    end
  end

  
  def round_to_next_5(n)
      if n % 5 == 0
        return n
      else 
        return n.round(-1)
      end
  end
  
  def download_blank_csv
    send_file(
      "#{Rails.root}/app/assets/data/blank_csv.csv",
      filename: "blank_csv.csv"
    )
  end
  
  def download_sample_data
    send_file(
      "#{Rails.root}/app/assets/data/sample_data.csv",
      filename: "sample_data.csv"
    )
  end
  
  def assign_session_data()
    
  end
end
