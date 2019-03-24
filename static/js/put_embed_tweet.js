function put_embed_tweet(embed_tweet_dict, with_media) {
     //var str = JSON.stringify(embed_dict, null, 2);
     //alert("with media "+with_media);
     if (with_media){
        //alert(embed_tweet_dict["embed_with_media"]);
        var content = '<div>'+ embed_tweet_dict["embed_with_media"]+'</div>'
     } else {
        //alert(embed_tweet_dict["embed_without_media"]);
        var content = '<div>'+ embed_tweet_dict["embed_without_media"]+'</div>'
     }
     document.write(content)
}