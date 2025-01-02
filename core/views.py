from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from core.models import FBGroup
from core.utils import upload_url_to_apify,update_data_to_db




class FetchGroupDataView(GenericAPIView):
    
    def post(self, request,*args,**kwargs):
        group_url = self.request.data.get('group_url')
        data = upload_url_to_apify(group_url)
        if data['status'] != "READY":
            return Response({"message": "Something went wrong"})

        group_id = group_url.split("/groups/")[-1].strip("/")
        FBGroup.objects.update_or_create(
            url=group_url,
            group_id=group_id,
            defaults={
                'webhook_id': data['webhook_id'],
                'run_id': data['run_id'],
                'defaultDatasetId': data['defaultDatasetId']
            }
        )
            

        return Response({"message": "Scraping job started. You will be notified once it's complete."})


class APifyWebhookView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        
       
        data = request.data
       
        run_id = data.get("run_id")
        fetch_data = update_data_to_db(run_id)
        if fetch_data:
            return Response({"message": "Data has been updated successfully."})
        return Response({"message": "Something went wrong."})
        
#    