def responseJSON(status_code, flag, message, result):
    ''' Fuction buat formating respon to json '''
    resp = {}
    resp['status_code'] = status_code
    resp['status'] = flag
    resp['message'] = message
    resp['result'] = result
    return resp

def responseJSON2(status_code, flag, message, result,result2):
    ''' Fuction buat formating respon to json '''
    resp = {}
    resp['status_code'] = status_code
    resp['status'] = flag
    resp['message'] = message
    resp['result'] = result
    resp['result2'] = result2
    return resp