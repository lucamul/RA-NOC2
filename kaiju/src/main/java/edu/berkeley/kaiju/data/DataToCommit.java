package edu.berkeley.kaiju.data;

import java.util.Map;

import edu.berkeley.kaiju.service.request.handler.KaijuServiceHandler;

public class DataToCommit {
    public Map<String,byte[]> values;
    public Long timestamp;

    public DataToCommit(Map<String,byte[]> values, Long timestamp){
        this.values = values;
        this.timestamp = timestamp;
    }
    
}
