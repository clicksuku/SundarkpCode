package com.sundarkp.PrintSafeApp.model;

public class FileUploadResponse {
        private String fileName;
        private String generateotpUrl;

    public String getFileName() {
        return this.fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getDownloadUri() {
        return this.generateotpUrl;
    }

    public void setDownloadUri(String generateotpUrl) {
        this.generateotpUrl = generateotpUrl;
    }
     
    
    
}
