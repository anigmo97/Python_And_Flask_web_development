from pymongo import MongoClient,errors
from bson.objectid import ObjectId
# from global_functions import change_dot_in_keys_for_bullet,change_bullet_in_keys_for_dot
import traceback
import json
import ast # to load query string to dict
from datetime import datetime
import re
from bson.code import Code

MONGO_HOST= 'mongodb://localhost/tweet'
client = MongoClient(MONGO_HOST)
db = client.twitterdb

current_collection = "tweets"
default_collection = "tweets"

###################### SPECIAL DOCS #######################################################
statistics_file_id = "statistics_file_id"
query_file_id = "query_file_id"
streamming_file_id = "streamming_file_id"
searched_users_file_id = "searched_users_file_id"
likes_list_file_id = "likes_list_file_id"
users_file_id = "users_file_id"

special_doc_ids = [statistics_file_id,query_file_id,streamming_file_id,searched_users_file_id,likes_list_file_id,users_file_id]









#################################################################################################################
############################################ GET INFO ###########################################################
#################################################################################################################


def get_users_screen_name_dict_of_tweet_ids(tweet_id_list,collection):
    cursor_resultados = db[collection].find({'_id': {'$in': tweet_id_list}},{'_id':1,'user.screen_name':1})
    dict_tweet_user = {}
    for e in cursor_resultados:
        dict_tweet_user[e["_id"]] = e["user"]["screen_name"]
    # print(dict_tweet_user)
    return dict_tweet_user

def get_users_screen_name_dict_of_tweet_ids_for_tops_in_statistics_file(statistics_file,collection):
    top_10_name_lists = ["global_most_favs_tweets","global_most_rt_tweets","local_most_replied_tweets","local_most_quoted_tweets"]
    tweet_id_list = []
    for top_list in top_10_name_lists:
        for e in statistics_file[top_list]:
            tweet_id_list.append(e[0])

    return  get_users_screen_name_dict_of_tweet_ids(tweet_id_list,collection)


def get_tweet_dict_by_tweet_id_using_regex(regex,collection):
    return  { x['_id'] : x for x in db[collection].find({'_id':{'$regex':regex, '$nin': special_doc_ids}})}

def get_likes_info_for_flask(collection,limit=0):
    """Returns a list of tweets from the collection that have its 'likes_info.likes_count_updated' field set to False"""
    lista_tweets = list(db[collection].find({"has_likes_info" : True,'_id': {'$nin': special_doc_ids }},{"likes_info":True}).limit(limit))
    print("[LIKES INFO FOR FLASK] {} tweets retrieved".format(len(lista_tweets)))
    return lista_tweets


def get_tweet_by_id(id_str,collection):
    return db[collection].find_one({'_id':id_str})

def get_collection_names():
    return db.collection_names()

def get_count_of_a_collection(collection):
    return db[collection].count()

#########################################################################################################################################
############################### SPECIAL DOCS MANAGEMENT #################################################################################
#########################################################################################################################################

def do_additional_actions_for_statistics_file(statistics_dict,collection):
    def delete_statistics_file():
        print("[MONGO STATISTICS WARN] Deleting statistics file")
        db[collection].remove({"_id":statistics_file_id})
        print("[MONGO STATISTICS WARN] Statistics file has been deleted")

    if statistics_dict["messages_count"]==0:
        print("[MONGO STATISTICS WARN] El fichero está corrupto messages_count=0 se recalcularán las estadísticas...")
        delete_statistics_file()
        return None
    elif get_count_of_a_collection(collection) not in range(statistics_dict["messages_count"],statistics_dict["messages_count"]+len(special_doc_ids)+1):
        print("[MONGO STATISTICS WARN] El fichero está corrupto messages_count={} database_count={}".format(statistics_dict["messages_count"],get_count_of_a_collection(collection)))
        delete_statistics_file()
        return None

    way_of_send_with_keys_with_dots =  change_bullet_in_keys_for_dot(statistics_dict["way_of_send_counter"])
    statistics_dict["way_of_send_counter"] = way_of_send_with_keys_with_dots
    return statistics_dict

def get_log_dict_for_special_file_id(file_id):
    aux = {
        statistics_file_id : { "upper_name" : "STATISTICS_FILE", "file_aux" :"Fichero de estadisticas" , "file_id" : statistics_file_id },
        query_file_id : { "upper_name" : "QUERY_FILE", "file_aux" :"Fichero de querys" , "file_id" : query_file_id },
        streamming_file_id : { "upper_name" : "STREAMMING_FILE", "file_aux" :"Fichero de busquedas por streamming" , "file_id" : streamming_file_id },
        searched_users_file_id : { "upper_name" : "SEARCHED_USERS_FILE", "file_aux" :"Fichero de usuarios buscados" , "file_id" : searched_users_file_id },
        users_file_id : { "upper_name" : "USERS_FILE", "file_aux" :"Fichero de usuarios" , "file_id" : users_file_id },
        likes_list_file_id : { "upper_name" : "LIKES_FILE", "file_aux" :"Fichero de likes" , "file_id" : likes_list_file_id }
        
    }
    return aux.get(file_id,None)

def _get_special_file(collection,file_id):    
    e = get_log_dict_for_special_file_id(file_id)
    cursor_resultados = db[(collection or "tweets")].find({"_id": e["file_id"]})
    file_list = [ x for x in cursor_resultados]
    if len(file_list) >1:
        raise Exception('[MONGO {} ERROR] Hay mas de un fichero con _id igual al {}: _id = {}'.format(e["upper_name"],e["file_aux"],e["file_id"]))
    elif len(file_list) == 1:
        print("[MONGO {} INFO] {} correctamente recuperado para la colección {}".format(e["upper_name"],e["file_aux"],collection))
        retrieved_file = file_list[0]
        if e["file_id"] != statistics_file_id:
            return retrieved_file
        else:
            return do_additional_actions_for_statistics_file(retrieved_file,collection)
    else:
        print("[MONGO {} INFO] No hay {} para la colección {}".format(e["upper_name"],e["file_aux"],collection))
        return None

def get_statistics_file_from_collection(collection):
    return _get_special_file(collection,statistics_file_id)

def get_query_file(collection):
    return _get_special_file(collection,query_file_id)

def get_streamming_file(collection):
    return _get_special_file(collection,streamming_file_id)

def get_searched_users_file(collection):
    return _get_special_file(collection,searched_users_file_id)

def get_likes_list_file(collection):
    return _get_special_file(collection,likes_list_file_id)

def get_users_file(collection):
    return _get_special_file(collection,users_file_id)


#########################################################################################################################################
##################################### AUXILIAR ##########################################################################################
#########################################################################################################################################
def replace_bullet_with_dot(word):
    return word.replace('•','.')

def replace_dot_with_bullet(word):
    return word.replace('.','•') 

def change_dot_in_keys_for_bullet(dicctionary):
    new_dict = {}
    for k,v in dicctionary.items():
        if "." in k:
            print("[CHANGE DOT FOR BULLET INFO] Changing '.' in key {} for '•'".format(k))
            new_key = replace_dot_with_bullet(k)
            new_dict[new_key] = v
        else:
            new_dict[k] = v
    return new_dict

def change_bullet_in_keys_for_dot(dicctionary):
    new_dict = {}
    for k,v in dicctionary.items():
        if "•" in k:
            print("[CHANGE BULLET FOR DOT INFO] Changing '•' in key {} for '.'".format(k))
            new_key = replace_bullet_with_dot(k)
            new_dict[new_key] = v
        else:
            new_dict[k] = v
    return new_dict