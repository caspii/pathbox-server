IMAGE=gcr.io/location-tracker-70ccd/pathbox
gcloud builds submit --tag $IMAGE
gcloud run deploy pathbox --image $IMAGE --platform managed