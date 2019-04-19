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
    
    @HR_series_a =  [[2, 100], [16, 100]]
    @HR_series_b =  [[2, 60], [16, 60]]
    
    @SBP_series_a =  [[2, 110], [16, 110]]
    @SBP_series_b =  [[2, 130], [16, 130]]
    @SBP_series_c =  [[2, 180], [16, 180]]
    
    
    @DBP_series_a =  [[2, 70], [16, 70]]
    @DBP_series_b =  [[2, 80], [16, 80]]
    @DBP_series_c =  [[2, 120], [16, 120]]
    
    @Temp_series_a =  [[2, 100], [16, 100]]
    @Temp_series_b =  [[2, 95], [16, 95]]
    
    @SP_series_a =  [[2, 90], [16, 90]]
    
    @patient_risk = 90
    @model1_risk = 0
    @model2_risk = 0
    @model2_risk = 0
    @model2_risk = 0
    
    @mdoel_variable1 = 'Heart Rate'
    @mdoel_variable2 = 'SpO2'
    
    @image_patient_risk = round_to_next_5(@patient_risk)
    @image_path = '/assets/risk_' + @image_patient_risk.to_s + '.jpg'
    
    @doctor_notes = "These are the doctors notes."
    @event_notes = "These are the event notes."
    @discharge_notes = "These are the discharge notes."
  end
  
  def create
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
end


