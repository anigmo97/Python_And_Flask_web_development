function put_embed_tweet(tweet_id,embed_dict, with_media) {
     //var str = JSON.stringify(embed_dict, null, 2);
     //alert("with media "+with_media);
     var registry = embed_dict[tweet_id];
     //alert(JSON.stringify(registry, null, 2))
     if (with_media && registry["embed_with_media"]!=null){
      //   alert(embed_tweet_dict["embed_with_media"]);
        var content = '<div class="d-flex justify-content-center hidden_tweet">'+ registry["embed_with_media"]+'</div>'
     } else {
      //   alert(embed_tweet_dict["embed_without_media"]);
        var content = '<div class="d-flex justify-content-center hidden_tweet">'+ registry["embed_without_media"]+'</div>'
     }
     document.write(content)
}