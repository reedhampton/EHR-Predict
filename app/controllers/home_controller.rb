require 'csv'


class HomeController < ApplicationController
  def index
    flash.clear
  end
  
  def results
    flash.clear
    flash[:success] = "Successful Precitive Analysis"
    
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
    
    @patient_risk = 90
    @model1_risk = 0
    @model2_risk = 0
    @model2_risk = 0
    @model2_risk = 0
    
    @mdoel_variable1 = 'Heart Rate'
    @mdoel_variable2 = 'SpO2'
    
    @image_patient_risk = round_to_next_5(@patient_risk)
    @image_path = '/assets/risk_' + @image_patient_risk.to_s + '.jpg'
    
    @doctor_notes = "Doctor text"
    @event_notes = "These are the event notes."
    @discharge_notes = "These are the discharge notes."
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
    
        #Run our cleaning scripts on the file
        @python_clean_data = "python /home/ec2-user/environment/EHR-Predict/lib/assets/clean_all_data.py";
        @python_return = `#{@python_clean_data}`;
        
        @python_model_connect = "python /home/ec2-user/environment/EHR-Predict/lib/assets/make_connection.py";
        @python_model_return = `#{@python_model_connect}`;
    
        #Call the Fancy Python Script
        
        
        #Get the returns from the Fancy python Script
        #Parse those returns
        #Put them in sessions
        
        #Delete teh CSV
        
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
