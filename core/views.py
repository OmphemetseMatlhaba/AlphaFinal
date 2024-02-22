from django.shortcuts import render
import os
from django.shortcuts import render, redirect
from .forms import CropPredictionForm
from .models import CropPrediction
import joblib
from django.conf import settings

def predict_crop(request):
    form = CropPredictionForm()
    predicted_crops = []  # Initialize the list to store predicted crops

    if request.method == 'POST':
        form = CropPredictionForm(request.POST)
        if form.is_valid():
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'naive_bayes_model.pkl')
            nb_model = joblib.load(model_path)
            input_data = [form.cleaned_data['nitrogen'], form.cleaned_data['phosphorus'],
                          form.cleaned_data['potassium'], form.cleaned_data['temperature'],
                          form.cleaned_data['humidity'], form.cleaned_data['pH'], form.cleaned_data['rainfall']]

            increments = [0, 1, -10, 4, 5, 6, -3, -4]  # Define increments here

            num_predictions = 1  # Define num_predictions here

            for increment in increments:
                new_data = [x + increment for x in input_data]
                prediction = nb_model.predict([new_data])[0]

                # Check if the prediction is unique before appending to the list
                if prediction not in predicted_crops:
                    predicted_crops.append(prediction)

                for _ in range(num_predictions - 1):  # Skip the inner loop if num_predictions is greater than 1
                    _ = nb_model.predict([new_data])[0]

    return render(request, 'predict/predict_crop.html', {'form': form, 'predicted_crops': predicted_crops})
