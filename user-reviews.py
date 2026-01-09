import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    
    # Extract review text from event (or use default)
    review_text = event.get('review', 'This is a default review for testing.')
    
    print(f"🔍 Analyzing sentiment for: '{review_text}'")
    
    try:
        # Analyze sentiment using Amazon Comprehend
        response = comprehend.detect_sentiment(
            Text=review_text,
            LanguageCode='en'
        )
        
        sentiment = response['Sentiment']
        positive_score = response['SentimentScore']['Positive']
        negative_score = response['SentimentScore']['Negative']
        neutral_score = response['SentimentScore']['Neutral']
        mixed_score = response['SentimentScore']['Mixed']
        
        # Log detailed results
        print(f"📊 Sentiment: {sentiment}")
        print(f"   Positive: {positive_score:.2%}")
        print(f"   Negative: {negative_score:.2%}")
        print(f"   Neutral:  {neutral_score:.2%}")
        print(f"   Mixed:    {mixed_score:.2%}")
        
        # Emoji summary for easy reading
        sentiment_emoji = {
            'POSITIVE': '✅',
            'NEGATIVE': '❌', 
            'NEUTRAL': '➖',
            'MIXED': '🔀'
        }
        print(f"🎯 RESULT: {sentiment_emoji.get(sentiment, '?')} {sentiment}")
        
    except ClientError as e:
        print(f"❌ Comprehend error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "review": review_text,
            "sentiment": sentiment,
            "scores": {
                "positive": f"{positive_score:.2%}",
                "negative": f"{negative_score:.2%}",
                "neutral": f"{neutral_score:.2%}",
                "mixed": f"{mixed_score:.2%}"
            }
        })
    }
