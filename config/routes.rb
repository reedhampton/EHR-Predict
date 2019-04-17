Rails.application.routes.draw do
  
  root 'home#index'
  
  get 'home', to: 'home#index'
  
  get 'results', to: 'home#results'
  
  get 'analysis', to: 'home#new'
  post 'analyze', to: 'home#create'
  
  get 'analysis/blank_csv', to: 'home#download_blank_csv'
  get 'analysis/sample_data', to: 'home#download_sample_data'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
