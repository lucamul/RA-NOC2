package edu.berkeley.kaiju.service.request.handler;

import java.util.Collection;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.beust.jcommander.internal.Maps;

import edu.berkeley.kaiju.KaijuServer;
import edu.berkeley.kaiju.config.Config;
import edu.berkeley.kaiju.data.DataItem;
import edu.berkeley.kaiju.exception.HandlerException;
import edu.berkeley.kaiju.net.routing.OutboundRouter;
import edu.berkeley.kaiju.service.request.RequestDispatcher;
import edu.berkeley.kaiju.service.request.message.KaijuMessage;
import edu.berkeley.kaiju.service.request.message.request.CommitPutAllRequest;
import edu.berkeley.kaiju.service.request.message.request.PreparePutAllRequest;
import edu.berkeley.kaiju.service.request.message.request.PutAllRequest;
import edu.berkeley.kaiju.service.request.message.response.KaijuResponse;
import edu.berkeley.kaiju.util.Timestamp;

public class ReadAtomicNOCBasedKaijuServiceHandler extends ReadAtomicKaijuServiceHandler{

    public ReadAtomicNOCBasedKaijuServiceHandler(RequestDispatcher dispatcher) {
        super(dispatcher);
    }

    public void addPrep(Collection<String> keys, long timestamp){
        synchronized(this){
            for(String key : keys){
                if(!KaijuServer.prep.containsKey(key) || KaijuServer.prep.get(key) < timestamp)
                    KaijuServer.prep.put(key, timestamp);
            }
        }
    }

    public void removePrep(Collection<String> keys,long timestamp){
        synchronized(this){
            for(String key:keys){
                if(KaijuServer.prep.containsKey(key) && KaijuServer.prep.get(key) == timestamp) KaijuServer.prep.remove(key);
            }
        }
    }

    
    private void addHct(int serverId, long hct){
        if(!KaijuServer.hcts.containsKey(serverId) || KaijuServer.hcts.get(serverId) < hct){
            KaijuServer.hcts.put(serverId, hct);
        }
    }

    @Override
    public void put_all(Map<String, byte[]> keyValuePairs) throws HandlerException {
        Long timestamp = Timestamp.assignNewTimestamp();
        return;
    }

    @Override
    public Map<String, byte[]> get_all(List<String> keys) throws HandlerException {
        try{
            return null;
        }catch(Exception e){
            throw new HandlerException("Error processing request",e);
        }
    }

    private void tester_read(Collection<KaijuResponse> responses){
        for(KaijuResponse response : responses){
            for(Map.Entry<String,DataItem> keyValuePair : response.keyValuePairs.entrySet()){
                if(keyValuePair != null && keyValuePair.getValue() != null && keyValuePair.getValue().getPrepTs() != Timestamp.NO_TIMESTAMP)
                    KaijuServiceHandler.logger.warn("TR: r(" + keyValuePair.getKey() + "," + ((Long)keyValuePair.getValue().getPrepTs()).toString() + "," + cid.get() + "," + tid.get() + ")");
            }
        }
    }


    

    @Override
    public DataItem instantiateKaijuItem(byte[] value, Collection<String> allKeys, long timestamp) {
        Map<String,Long> lasts = new HashMap<String,Long>();
        DataItem item =  new DataItem(timestamp, value);
        return item;
    }
    
}
