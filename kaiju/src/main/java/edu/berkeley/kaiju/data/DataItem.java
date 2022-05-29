package edu.berkeley.kaiju.data;

import edu.berkeley.kaiju.util.Timestamp;
import org.apache.hadoop.util.bloom.BloomFilter;

import java.sql.Time;
import java.util.Collection;
import java.util.Map;

import com.esotericsoftware.kryo.serializers.DefaultArraySerializers.BooleanArraySerializer;

/*
 Since we implemented so many different algorithms for the paper, this
 class bloated quite a bit. Annotations inline.
 */
public class DataItem {
    // Every item has a version
    private long timestamp = Timestamp.NO_TIMESTAMP;
    private byte[] value;

    // Used in RAMP-Fast
    private Collection<String> transactionKeys = null;

    // Used in RAMP-Hybrid
    private BloomFilter bloomTransactionKeys = null;

    private String cid;
    private Boolean flag;
    private Long prepTs = Timestamp.NO_TIMESTAMP;

    public DataItem(long timestamp, byte[] value) {
        this.timestamp = timestamp;
        this.value = value;
    }

    public DataItem(long timestamp, byte[] value, Collection<String> transactionKeys) {
        this(timestamp, value);
        this.transactionKeys = transactionKeys;
    }

    public DataItem(long timestamp, byte[] value, BloomFilter bloomTransactionKeys) {
        this(timestamp, value);
        this.bloomTransactionKeys = bloomTransactionKeys;
    }

    public DataItem() {}

    public long getTimestamp() {
        return timestamp;
    }

    public boolean hasTransactionKeys() {
        return transactionKeys != null;
    }

    public byte[] getValue() {
        return value;
    }

    public String getCid(){
        return cid;
    }

    public void setCid(String cid){
        this.cid = cid;
    }
    
    public boolean getFlag(){
        return this.flag;
    }

    public void setFlag(boolean flag){
        this.flag = flag;
    }

    public void setPrepTs(long prepTs){
        this.prepTs = prepTs;
    }

    public long getPrepTs(){
        return this.prepTs;
    }

    public void setTimestamp(long timestamp){
        this.timestamp = timestamp;
    }

    public Collection<String> getTransactionKeys() {
        return transactionKeys;
    }

    public BloomFilter getBloomTransactionKeys() {
        return bloomTransactionKeys;
    }

    public static DataItem getNullItem() {
        return new DataItem(Timestamp.NO_TIMESTAMP, new byte[0]);
    }
}