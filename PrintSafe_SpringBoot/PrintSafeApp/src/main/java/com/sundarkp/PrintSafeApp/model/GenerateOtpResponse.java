package com.sundarkp.PrintSafeApp.model;

public class GenerateOtpResponse {
    private String fileCode;
    private String downloadurl;

    public String getFileCode() {
        return this.fileCode;
    }

    public void setFileCode(String fileCode) {
        this.fileCode = fileCode;
    }

    public String getDownloadurl() {
        return this.downloadurl;
    }

    public void setDownloadurl(String downloadurl) {
        this.downloadurl = downloadurl;
    }    
}
