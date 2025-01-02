from apify_client import ApifyClient
from core.models import FBGroup, Post
from decouple import config
APIFY_TOKEN = config("APIFY_TOKEN")
client = ApifyClient(APIFY_TOKEN)
def upload_url_to_apify(url_to_scrap):
    
    run_input = {"startUrls": [{"url": url_to_scrap}], "viewOption": "CHRONOLOGICAL"}

    run = client.actor("apify/facebook-groups-scraper").start(run_input=run_input)
    run_id = run["id"]
    webhook_data = {
        "event_types": ["ACTOR.RUN.SUCCEEDED"],
        "request_url": "https://8395-123-201-245-158.ngrok-free.app/api/apify_webhook/",
        "payload_template": f'{{"run_id": "{run_id}"}}',
        "actor_id": config("ACTOR_ID"),
        "do_not_retry": True,
    }

    webhook = client.webhooks().create(**webhook_data)
    webhook_id = webhook["id"]
    data = {
        "run_id": run["id"],
        "status": run["status"],
        "defaultDatasetId": run["defaultDatasetId"],
        "webhook_id": webhook_id,
    }
    return data



def update_data_to_db(run_id):
    try:
        
        group = FBGroup.objects.filter(run_id=run_id).first()
        if not group:
            print(f"Group with run_id {run_id} not found.")
            return False

       
        post_list = []

       
        for item in client.dataset(group.defaultDatasetId).iterate_items():
            url = item.get('url', '')
            post_id = url.split("/permalink/")[-1].strip("/")
            
            
            if Post.objects.filter(post_id=post_id).exists():
                continue

          
            post = Post(
                group=group,  
                content=item.get('text', ''), 
                user_id=item.get('user', {}).get('id', ''), 
                user_name=item.get('user', {}).get('name', ''),  
                facebook_post_id=item.get('facebookId', ''),  
                created_at=item.get('time', ''),  
                likes_count=item.get('likesCount', 0),  
                shares_count=item.get('sharesCount', 0), 
                comments_count=item.get('commentsCount', 0),
                post_url=item.get('url', ''),
                post_id=post_id
            )
            post_list.append(post)

       
        if post_list:
            Post.objects.bulk_create(post_list)

        group.is_updated = True
        group.name = item.get('groupTitle', group.name)  
        group.save(update_fields=['is_updated', 'name'])

        return True
    except Exception as e:
        
        print(f"Error during update: {e}")
        return False
