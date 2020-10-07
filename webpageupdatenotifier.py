# Script to notfy me for any changes on a lsit of webpages
# shows what changed during this time
# will be adding to cron jobs to run on every system startup

#todo
# ssl verify

import yaml
import hashlib
import random,time,os
from requests_html import HTMLSession
import traceback
from termcolor import colored
import urllib3
urllib3.disable_warnings()

def load_file(filename="config.yaml"):
    try :
        with open(filename, "r") as stream:
            try :
                cfg = yaml.safe_load(stream)
                # print(cfg)
            except yaml.YAMLError as err :
                print(err)
                exit()
            return cfg
    except FileNotFoundError :
        print("filenotfound")
        return None


def generateHash(x):
    hasher=hashlib.sha256()
    hasher.update(bytes(x,'utf-8'))

    return hasher.hexdigest()


def write_hashes_generated(hsdhdict,filename="hashes_generated.yaml"):
    with open(filename, "w") as stream:
        try :
            write = yaml.dump({"hashes":hsdhdict},stream)
            print(colored("generated hashes written to file","green"))
            
        except yaml.YAMLError as err :
            print(colored(err,"red"))
            exit()
    
def comparinator(saved_hashes,generated_hashes,showhash=True):
    common_keys= saved_hashes.keys() & generated_hashes.keys()
    onlyin_saved = saved_hashes.keys() - generated_hashes.keys()
    onlyin_generated = generated_hashes.keys() - saved_hashes.keys()
    common_pairs= saved_hashes.items() & generated_hashes.items()
    print(colored("NO changes for the following websites","blue"))

    for i,e in enumerate(common_pairs):
        print(colored( ( str(i+1)+") " + str(e[0]) ), "blue"))
        if showhash == True :
            print(saved_hashes[e[0]],"==",generated_hashes[e[0]]) # common_pairs is a set of tuples

    print("\n")
    print(colored("changes in the following webpages:","green"))
    for key in common_keys:
        if saved_hashes[key] != generated_hashes[key]:
            print(colored(key,"yellow"))
            if showhash == True:
                print(saved_hashes[key],"!=",generated_hashes[key])
                print()

            

    return onlyin_generated,onlyin_saved
    


    

    


if __name__=="__main__":
    cfg=load_file("config.yaml")
    if cfg == None:
        print("NO config file")
        exit()
    nonjsurls=cfg["urls"]["nonjs"]
    jsurls=cfg["urls"]["js"]
    useragent=random.choice(cfg["useragents"])
    headers={"User-Agent":useragent}
    saved_hashes=load_file("hashes2.yaml")
    if not(saved_hashes == None):
        saved_hashes=saved_hashes["hashes"]
    hashes_generated={}
    session = HTMLSession()
    reqs=[]



    for url in nonjsurls:
        try :
            print("Generating session for url:",url)
            r=session.get(url,headers=headers,timeout=5,verify=False)#  todo verify 
            hashval=generateHash(r.text)
            hashes_generated[url]=hashval
            print(colored(hashval,"green"))
            if(not(r.ok)):
                print(colored(("Got the page with code:"+str(r.status_code)),"red"))
                print(colored("skipping this url","blue"))
                continue
        except :
            print(colored("error occured / timeout skipping this:-----\n","red"))
            print(traceback.print_exc() )
            continue
    
    if saved_hashes == None:
        print(colored("No saved hashes found","yellow"))
        write_hashes_generated(hashes_generated,"hashes2.yaml")
        print("hashes recorded exiting ")
        exit()

    onlyin_generated,onlyin_saved=comparinator(saved_hashes,hashes_generated)
    if onlyin_generated != None:
        print("adding and saving new_hashes generated/ new_urls found in config")
        for i in onlyin_generated:
            saved_hashes[i]=hashes_generated[i]
            print(i)
        write_hashes_generated(saved_hashes,"hashes2.yaml")

    





































# for r in reqs :
#     print(type(r),"-----------")
#     try :
#         print("-------")
#         ren=r.html.render()
#         print(ren)
#     except :   
#         print("error occured during rendering",  traceback.print_exc() )
#         continue
#     # hashval=generateHash(ren.text)
#     # print(hashval)










    # 100: continue
    # 101: switching_protocols
    # 102: processing
    # 103: checkpoint
    # 122: uri_too_long, request_uri_too_long
    # 200: ok, okay, all_ok, all_okay, all_good, \o/, ✓
    # 201: created
    # 202: accepted
    # 203: non_authoritative_info, non_authoritative_information
    # 204: no_content
    # 205: reset_content, reset
    # 206: partial_content, partial
    # 207: multi_status, multiple_status, multi_stati, multiple_stati
    # 208: already_reported
    # 226: im_used
    # 300: multiple_choices
    # 301: moved_permanently, moved, \o-
    # 302: found
    # 303: see_other, other
    # 304: not_modified
    # 305: use_proxy
    # 306: switch_proxy
    # 307: temporary_redirect, temporary_moved, temporary
    # 308: permanent_redirect, resume_incomplete, resume
    # 400: bad_request, bad
    # 401: unauthorized
    # 402: payment_required, payment
    # 403: forbidden
    # 404: not_found, -o-
    # 405: method_not_allowed, not_allowed
    # 406: not_acceptable
    # 407: proxy_authentication_required, proxy_auth, proxy_authentication
    # 408: request_timeout, timeout
    # 409: conflict
    # 410: gone
    # 411: length_required
    # 412: precondition_failed, precondition
    # 413: request_entity_too_large
    # 414: request_uri_too_large
    # 415: unsupported_media_type, unsupported_media, media_type
    # 416: requested_range_not_satisfiable, requested_range, range_not_satisfiable
    # 417: expectation_failed
    # 418: im_a_teapot, teapot, i_am_a_teapot
    # 421: misdirected_request
    # 422: unprocessable_entity, unprocessable
    # 423: locked
    # 424: failed_dependency, dependency
    # 425: unordered_collection, unordered
    # 426: upgrade_required, upgrade
    # 428: precondition_required, precondition
    # 429: too_many_requests, too_many
    # 431: header_fields_too_large, fields_too_large
    # 444: no_response, none
    # 449: retry_with, retry
    # 450: blocked_by_windows_parental_controls, parental_controls
    # 451: unavailable_for_legal_reasons, legal_reasons
    # 499: client_closed_request
    # 500: internal_server_error, server_error, /o\, ✗
    # 501: not_implemented
    # 502: bad_gateway
    # 503: service_unavailable, unavailable
    # 504: gateway_timeout
    # 505: http_version_not_supported, http_version
    # 506: variant_also_negotiates
    # 507: insufficient_storage
    # 509: bandwidth_limit_exceeded, bandwidth
    # 510: not_extended
    # 511: network_authentication_required, network_auth, network_authentication