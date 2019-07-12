from pymongo import MongoClient,errors,ASCENDING,DESCENDING
from pymongo.collation import Collation
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
#users_file_id = "users_file_id"

special_doc_ids = [statistics_file_id,query_file_id,streamming_file_id,searched_users_file_id,likes_list_file_id]









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
    lista_tweets = list(db[collection].find({"has_likes_info" : True,'_id': {'$nin': special_doc_ids,"$regex":"^(?!likes_count_file)" }},{"likes_info":True}).limit(limit))
    print("[LIKES INFO FOR FLASK] {} tweets retrieved".format(len(lista_tweets)))
    return lista_tweets


def get_tweet_by_id(id_str,collection):
    return db[collection].find_one({'_id':id_str})

def get_collection_names():
    return db.collection_names()

def get_count_of_a_collection(collection):
    return db[collection].count()

def get_number_of_likes_count_files_cursor(collection):
    """Returns likes count files of  collection"""
    return db[(collection)].find({"_id": {"$regex":"^(likes_count_file)"}}).count()
    
def get_likes_count_files_cursor(collection):
    """Returns likes count files of  collection"""
    return db[(collection)].find({"_id": {"$regex":"^(likes_count_file)"}})

def get_likes_count_files(collection):
    """Returns likes count files of  collection"""
    cursor_resultados = db[(collection)].find({"_id": {"$regex":"^(likes_count_file)"}}).sort("_id",ASCENDING).collation(Collation(locale="es",numericOrdering=True))
    return [ x for x in cursor_resultados]

def get_likes_count_files_dict(collection):
    """Returns likes count files of  collection"""
    #cursor_resultados = db[(collection)].find({"_id": {"$regex":"^(likes_count_file)"}}).sort("_id",ASCENDING).collation(Collation(locale="es",numericOrdering=True))
    cursor_resultados = db[(collection)].find({"_id": {"$regex":"^(likes_count_file)"}})
    return { x[0]:x[1] for x in enumerate(cursor_resultados)}

def get_likes_count_files_dict_with_id_as_key(collection):
    """Returns likes count files of  collection"""
    #cursor_resultados = db[(collection)].find({"_id": {"$regex":"^(likes_count_file)"}}).sort("_id",ASCENDING).collation(Collation(locale="es",numericOrdering=True))
    cursor_resultados = db[(collection)].find({"_id": {"$regex":"^(likes_count_file)"}})
    return { x["_id"] : x for x in cursor_resultados}

def get_tweets_of_a_user_from_collecton(screen_name,collection):
    return db[collection].find({"user.screen_name": screen_name, "has_likes_info":True})

def get_num_of_captured_likes_for_user(screen_name,collection):
    cursor_resultados = db[collection].find({"user.screen_name": screen_name})
    likes_capturados = 0
    for e in cursor_resultados:
        if e["has_likes_info"]:
            likes_capturados+= len(e["likes_info"]["users_who_liked"])
    return likes_capturados

def get_num_of_captured_likes_per_party(collection):
    likes_count_files = get_likes_count_files(collection)
    captured_likes_tweets = {
        "PP":0,
        "PSOE":0,
        "PODEMOS":0,
        "CIUDADANOS":0,
        "VOX":0,
        "COMPROMIS":0
    }
    for e in likes_count_files:
        for x in e:
            if x != "_id":
                registry = e[x]
                captured_likes_tweets["PP"] += registry["likes_to_PP"]
                captured_likes_tweets["PSOE"] += registry["likes_to_PSOE"]
                captured_likes_tweets["PODEMOS"] +=registry["likes_to_PODEMOS"]
                captured_likes_tweets["CIUDADANOS"] += registry["likes_to_CIUDADANOS"]
                captured_likes_tweets["COMPROMIS"]+= registry["likes_to_COMPROMIS"]
                captured_likes_tweets["VOX"] +=  registry["likes_to_VOX"]

    return captured_likes_tweets

def get_likes_count_files_by_num(num,collection):
    """Returns likes count files of  collection"""
    return db[(collection)].find({"_id": {"$regex":"^(likes_count_file_id_{})".format(num)}})[0]

def get_searched_user_registry_info_for_ui(screen_name,collection):
    cursor_resultados = get_tweets_of_a_user_from_collecton(screen_name,collection)
    users_dict = {}

    for tweet in cursor_resultados:
        for user_id in tweet["likes_info"]["users_who_liked"]:
            if tweet["likes_info"]["users_who_liked"][user_id]["counted"]:
                if user_id in users_dict:
                    users_dict[user_id]["num_likes"] += 1
                else:
                    users_dict[user_id]={}
                    users_dict[user_id]["user_id"] = tweet["likes_info"]["users_who_liked"][user_id]["user_id"]
                    users_dict[user_id]["user_screen_name"] = tweet["likes_info"]["users_who_liked"][user_id]["user_screen_name"]
                    users_dict[user_id]["num_likes"] = 1
    
    num_of_likes_count_files = get_number_of_likes_count_files_cursor(collection)
    num_verified = 0
    num_no_verified = 0
    for user_id in users_dict:
        for i in range(num_of_likes_count_files):
            f = get_likes_count_files_by_num(i,collection)
            if user_id in f:
                print(f[user_id])
                users_dict[user_id]["joined"] = f[user_id].get("joined","desconocido")
                users_dict[user_id]["verified"] = f[user_id].get("verified",False)
                if f[user_id].get("verified",False):
                    num_verified+=1
                else:
                    num_no_verified += 1
                users_dict[user_id]["tweets"] = f[user_id].get("tweets",0)
    
    return users_dict,num_verified,num_no_verified


#########################################################################################################################################
############################### SPECIAL DOCS MANAGEMENT #################################################################################
#########################################################################################################################################

def do_additional_actions_for_statistics_file(statistics_dict,collection):
    """Do a preprocess to treat the keys with '.' """
    print("[MONGO STATISTICS INFO] Changing bullets for dots")
    way_of_send_with_keys_with_dots =  change_bullet_in_keys_for_dot(statistics_dict["way_of_send_counter"])
    statistics_dict["way_of_send_counter"] = way_of_send_with_keys_with_dots
    return statistics_dict

def get_log_dict_for_special_file_id(file_id):
    aux = {
        statistics_file_id : { "upper_name" : "STATISTICS_FILE", "file_aux" :"Fichero de estadisticas" , "file_id" : statistics_file_id },
        query_file_id : { "upper_name" : "QUERY_FILE", "file_aux" :"Fichero de querys" , "file_id" : query_file_id },
        streamming_file_id : { "upper_name" : "STREAMMING_FILE", "file_aux" :"Fichero de busquedas por streamming" , "file_id" : streamming_file_id },
        searched_users_file_id : { "upper_name" : "SEARCHED_USERS_FILE", "file_aux" :"Fichero de usuarios buscados" , "file_id" : searched_users_file_id },
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