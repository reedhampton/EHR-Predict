require 'csv'


class HomeController < ApplicationController
  def index
    flash.clear
  end
  
  def results
    flash.clear
    flash[:success] = "Successful Precitive Analysis"
    
    # for csv.count()
    # get start time
    # get end time
    # apply to series
    table = CSV.read("#{Rails.root}/uploads/Patient Data.csv", headers: true)
    @data_start_time = table['charttime'].values_at(0)
    @data_end_time = table['charttime'].values_at(-1)
    time = table['charttime']
    hr = table['heart_rate']
    bp = table['abp_systolic']
    gs = table['gcs_total']
    pl = table['platelets']
    
    @HR_series_data = [time, hr].transpose
    @HR_series_a =  [[@data_start_time, 100], [@data_end_time, 100]]
    @HR_series_b =  [[@data_start_time, 60], [@data_end_time, 60]]
    
    @SBP_series_data = [time, bp].transpose
    @SBP_series_a =  [[@data_start_time, 110], [@data_end_time, 110]]
    @SBP_series_b =  [[@data_start_time, 130], [@data_end_time, 130]]
    @SBP_series_c =  [[@data_start_time, 180], [@data_end_time, 180]]
   
    @DBP_series_data = [time, bp].transpose
    @DBP_series_a =  [[@data_start_time, 70], [@data_end_time, 70]]
    @DBP_series_b =  [[@data_start_time, 80], [@data_end_time, 80]]
    @DBP_series_c =  [[@data_start_time, 120], [@data_end_time, 120]]
    
    @Temp_series_data = [time, gs].transpose
    @Temp_series_a =  [[@data_start_time, 100], [@data_end_time, 100]]
    @Temp_series_b =  [[@data_start_time, 95], [@data_end_time, 95]]
    
    @SP_series_data = [time, pl].transpose
    @SP_series_a =  [[@data_start_time, 90], [@data_end_time, 90]]
    
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
    #Uploads the CSV into the /uploads directory
    uploaded_io = params[:user_input][:data]
    
    # Validate the file format, redirect if not a CSV
    if uploaded_io.content_type != "application/octet-stream"
      flash[:alert] = "Incorrect File Type"
      redirect_to '/analysis'
    #Save the file and move on
    else
      File.open(Rails.root.join('uploads', 'Patient Data.csv'), 'wb') do |file|
        file.write(uploaded_io.read)
      end
  
      #Call the Fancy Python Script
      #Get the returns from the Fancy python Script
      #Parse those returns
      #Put them in sessions
      assign_session_data() #does nothing right now
      
      #Delete teh CSV
      
      redirect_to '/results'
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




