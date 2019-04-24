Rails.application.routes.draw do
  
  root 'home#index'
  
  get 'analysis', to: 'home#index'
  
  get 'results', to: 'home#results'
  
  post 'analyze', to: 'home#create'
  
  get 'analysis/blank_csv', to: 'home#download_blank_csv'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
