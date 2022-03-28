package edu.berkeley.kaiju.data;

import edu.berkeley.kaiju.util.Timestamp;
import org.apache.hadoop.util.bloom.BloomFilter;

import java.util.Collection;
import java.util.List;
public class LastValue {
    private long timestamp = Timestamp.NO_TIMESTAMP;
    private List<String> keys;

    public LastValue(long timestamp, List<String> keys) {
        this.timestamp = timestamp;
        this.keys = keys;
    }

    public long getTimestamp(){
        return this.timestamp;
    }

    public List<String> getKeys(){
        return this.keys;
    }

    public Boolean isIn(String key){
        return this.keys.contains(key);
    }

    public Boolean isEmpty(){
        return this.keys.isEmpty();
    }
}
