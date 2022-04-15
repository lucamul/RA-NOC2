package edu.berkeley.kaiju.service.request.message.request;

import edu.berkeley.kaiju.config.Config;
import edu.berkeley.kaiju.config.Config.ReadAtomicAlgorithm;
import edu.berkeley.kaiju.exception.KaijuException;
import edu.berkeley.kaiju.service.LockManager;
import edu.berkeley.kaiju.service.MemoryStorageEngine;
import edu.berkeley.kaiju.service.request.message.KaijuMessage;
import edu.berkeley.kaiju.service.request.message.response.KaijuResponse;

public class CommitPutAllRequest extends KaijuMessage implements IKaijuRequest {
    public long timestamp;

    private CommitPutAllRequest() {}

    public CommitPutAllRequest(long timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public KaijuResponse processRequest(MemoryStorageEngine storageEngine, LockManager lockManager) throws
                                                                                                    KaijuException {
        storageEngine.commit(timestamp);
        if(Config.getConfig().readatomic_algorithm == ReadAtomicAlgorithm.CONST_ORT){
            KaijuResponse response = new KaijuResponse();
            response.setHct(storageEngine.getHCT());
            response.senderID = Config.getConfig().server_id;
            return response;
        }
        return new KaijuResponse();
    }
}