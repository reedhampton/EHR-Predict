class HomeController < ApplicationController
  def index
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
    @nurse_notes = "These are the nurse notes."
    @discharge_notes = "These are the discharge notes."
    
  end
  
  def round_to_next_5(n)
      if n % 5 == 0
        return n
      else 
        return n.round(-1)
      end
  end
end


