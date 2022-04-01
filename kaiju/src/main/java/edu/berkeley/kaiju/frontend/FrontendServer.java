package edu.berkeley.kaiju.frontend;

import com.esotericsoftware.kryo.KryoException;
import com.google.common.collect.Maps;
import com.yammer.metrics.Timer;

import edu.berkeley.kaiju.KaijuServer;
import edu.berkeley.kaiju.config.Config;
import edu.berkeley.kaiju.config.Config.ReadAtomicAlgorithm;
import edu.berkeley.kaiju.data.DataItem;
import edu.berkeley.kaiju.frontend.request.ClientGetAllRequest;
import edu.berkeley.kaiju.frontend.request.ClientPutAllRequest;
import edu.berkeley.kaiju.frontend.request.ClientRequest;
import edu.berkeley.kaiju.frontend.response.ClientError;
import edu.berkeley.kaiju.frontend.response.ClientGetAllResponse;
import edu.berkeley.kaiju.frontend.response.ClientPutAllResponse;
import edu.berkeley.kaiju.frontend.response.ClientResponse;
import edu.berkeley.kaiju.service.request.handler.KaijuServiceHandler;
import edu.berkeley.kaiju.service.request.handler.ReadAtomicKaijuServiceHandler;
import edu.berkeley.kaiju.service.request.message.response.KaijuResponse;
import edu.berkeley.kaiju.util.KryoSerializer;
import edu.berkeley.kaiju.util.Timestamp;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.net.InetSocketAddress;
import java.nio.channels.Channels;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class FrontendServer {
    private static Logger logger = LoggerFactory.getLogger(FrontendServer.class);
    private ServerSocketChannel serverSocket;
    private KaijuServiceHandler handler;
    
    public FrontendServer(KaijuServiceHandler handler, int port) throws IOException {
        this.serverSocket = ServerSocketChannel.open();
        serverSocket.socket().bind(new InetSocketAddress(port));
        this.handler = handler;
    }

    private boolean canAdd(String key, long timestamp){
        return (!KaijuServer.last.containsKey(key) || KaijuServer.last.get(key) < timestamp);
    }

    public void addLast(String key, long timestamp, Collection<String> transactionKeys){
        if(canAdd(key, timestamp)){
            synchronized(this){
                KaijuServer.last.put(key, timestamp);
                transactionKeys.forEach(k -> {
                    if(canAdd(k, timestamp)) KaijuServer.last.put(k, timestamp);
                });
            }
        }
    }

    public long getLastTimestamp(String key){
        return KaijuServer.last.getOrDefault(key, Timestamp.NO_TIMESTAMP);
    }

    public void serve() {
        logger.info("Listening to external connections on "+serverSocket);

        (new FrontendConnectionServer(serverSocket, handler)).run();
    }

    private class FrontendConnectionServer implements Runnable {
        ServerSocketChannel serverSocket;
        KaijuServiceHandler handler;
        private FrontendConnectionServer(ServerSocketChannel serverSocket, KaijuServiceHandler handler) {
            this.serverSocket = serverSocket;
            this.handler = handler;
        }

        @Override
        public void run() {
            while(true) {
                try {
                    SocketChannel clientSocket = serverSocket.accept();

                    new Thread(new FrontendConnectionHandler(clientSocket, handler)).start();
                } catch(IOException e) {
                    logger.warn("Error accepting socket on "+serverSocket, e);
                }
            }
        }
    }
    private class FrontendConnectionHandler implements Runnable {
        KryoSerializer serializer = new KryoSerializer();
        KaijuServiceHandler handler = null;
        SocketChannel clientSocket = null;

        public FrontendConnectionHandler(SocketChannel clientSocket, KaijuServiceHandler handler) {
            this.clientSocket = clientSocket;
            serializer.setInputStream(Channels.newInputStream(clientSocket));
            serializer.setOutputStream(Channels.newOutputStream(clientSocket));
            this.handler = handler;
        }

        @Override
        public void run() {
            try {
                while(true) {
                    Object request = serializer.getObject();

                    if(request instanceof String) {
                        if(request.equals("EXIT")) {
                            clientSocket.close();
                            return;
                        }
                    }
                    if(Config.getConfig().readatomic_algorithm == ReadAtomicAlgorithm.LORA){
                        if(request instanceof ClientGetAllRequest){
                            Timer.Context context = KaijuServiceHandler.getAllTimer.time();
                            List<String> keys = ((ClientGetAllRequest)request).keys;
                            Map<String,Long> keyPairs = Maps.newHashMap();
                            keys.forEach(k -> {
                                long ts = getLastTimestamp(k);
                                if(ts != Timestamp.NO_TIMESTAMP)
                                    keyPairs.put(k, getLastTimestamp(k));
                            });
                            Collection<KaijuResponse> responses = ((ReadAtomicKaijuServiceHandler) this.handler.handler).fetch_by_version_from_server(keyPairs);
                            Map<String,byte[]> keyValuePairs = new HashMap<String,byte[]>();
                            context.stop();
                            for(KaijuResponse response : responses){
                                for(Map.Entry<String,DataItem> entry : response.keyValuePairs.entrySet()){
                                    if(entry == null || entry.getValue() == null || entry.getValue().getValue() == null) continue;
                                    keyValuePairs.put(entry.getKey(), entry.getValue().getValue());
                                    if(entry.getValue().getTransactionKeys() == null) continue;
                                    addLast(entry.getKey(), entry.getValue().getTimestamp(), entry.getValue().getTransactionKeys());
                                }
                            }
                            ClientResponse response = new ClientGetAllResponse(keyValuePairs);
                            serializer.serialize(response);
                        }else if(request instanceof ClientPutAllRequest){
                            long timestamp = handler.lora_put_all(((ClientPutAllRequest)request).keyValuePairs);
                            Collection<String> keys = ((ClientPutAllRequest)request).keyValuePairs.keySet();
                            synchronized(this){
                                keys.forEach(k -> {
                                    if(canAdd(k, timestamp)) KaijuServer.last.put(k, timestamp);
                                });
                            }
                            ClientResponse response = new ClientPutAllResponse();
                            serializer.serialize(response);
                        }
                    }else{
                        ClientResponse response = handler.processRequest((ClientRequest) request);
                        serializer.serialize(response);
                    }
                }
            } catch (KryoException e) {
                logger.error("Kryo error with client "+clientSocket, e);

                try {
                    clientSocket.close();
                } catch(IOException ex) {
                    logger.error("Exception closing connection: ", ex);
                }
            } catch (Exception e) {
                logger.error("Error executing request for client "+clientSocket, e);
                StringWriter sw = new StringWriter();
                PrintWriter pw = new PrintWriter(sw);
                e.printStackTrace(pw);

                try {
                    serializer.serialize(new ClientError(e+" "+sw.toString()));
                } catch (IOException ioe) {
                    logger.error("Error executing serialize for client error", ioe);
                }

            }
        }
    }
}
