package edu.berkeley.kaiju.service.request.message.request;

import edu.berkeley.kaiju.config.Config;
import edu.berkeley.kaiju.config.Config.ReadAtomicAlgorithm;
import edu.berkeley.kaiju.data.DataItem;
import edu.berkeley.kaiju.exception.KaijuException;
import edu.berkeley.kaiju.service.LockManager;
import edu.berkeley.kaiju.service.MemoryStorageEngine;
import edu.berkeley.kaiju.service.request.message.KaijuMessage;
import edu.berkeley.kaiju.service.request.message.response.KaijuResponse;

import java.util.Map;

public class PutAllRequest extends KaijuMessage implements IKaijuRequest {
    public Map<String, DataItem> keyValuePairs;

    private PutAllRequest() {}

    public PutAllRequest(Map<String, DataItem> keyValuePairs) {
        this.keyValuePairs = keyValuePairs;
    }

    @Override
    public KaijuResponse processRequest(MemoryStorageEngine storageEngine, LockManager lockManager) throws
                                                                                                    KaijuException {
        if(Config.getConfig().readatomic_algorithm == ReadAtomicAlgorithm.CONST_ORT){
            Map<String,DataItem> ret = storageEngine.getAllOra(keyValuePairs);
            KaijuResponse res =  new KaijuResponse(ret);
            res.senderID = Config.getConfig().server_id;
            return res;
        }
        storageEngine.putAll(keyValuePairs);
        return new KaijuResponse();
    }
}