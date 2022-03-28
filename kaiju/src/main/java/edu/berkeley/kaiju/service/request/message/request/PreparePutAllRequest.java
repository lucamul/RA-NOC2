package edu.berkeley.kaiju.service.request.message.request;

import edu.berkeley.kaiju.config.Config;
import edu.berkeley.kaiju.config.Config.ReadAtomicAlgorithm;
import edu.berkeley.kaiju.data.DataItem;
import edu.berkeley.kaiju.exception.KaijuException;
import edu.berkeley.kaiju.service.LockManager;
import edu.berkeley.kaiju.service.MemoryStorageEngine;
import edu.berkeley.kaiju.service.MemoryStorageEngine.KeyTimestampPair;
import edu.berkeley.kaiju.service.request.message.KaijuMessage;
import edu.berkeley.kaiju.service.request.message.response.KaijuResponse;

import java.util.Map;

import com.google.common.collect.Lists;

public class PreparePutAllRequest extends KaijuMessage implements IKaijuRequest {
    public Map<String, DataItem> keyValuePairs;

    private PreparePutAllRequest() {}

    public PreparePutAllRequest(Map<String, DataItem> keyValuePairs) {
        this.keyValuePairs = keyValuePairs;
    }

    @Override
    public KaijuResponse processRequest(MemoryStorageEngine storageEngine, LockManager lockManager) throws
                                                                                                    KaijuException {
        storageEngine.prepare(keyValuePairs);
        long time = System.currentTimeMillis();
        for(Map.Entry<String,DataItem> entry : keyValuePairs.entrySet()){
            storageEngine.timesPerVersion.putIfAbsent(storageEngine.createNewKeyTimestampPair(entry.getKey(), entry.getValue().getTimestamp()), time);
            if(storageEngine.latestTime.containsKey(entry.getKey()) && storageEngine.latestTime.get(entry.getKey()) < time){
                storageEngine.latestTime.replace(entry.getKey(),time);
            }else{
                storageEngine.latestTime.put(entry.getKey(), time);
            }
        }
        return new KaijuResponse();
    }
}