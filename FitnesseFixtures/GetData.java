package things2dofixtures;

import java.io.IOException;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class GetData {
	private String name = null;
	private String category = null;
	private String createdBy = null;
	private String address = null;
	private String phone = null;
	private String descr = null;
	private String url = null;
	private String email = null;
	private double lat = 0.0;
	private double lon = 0.0;
	private int rating = 0;
	private String review = null;

	public GetData(){
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setCategory(String category) {
		this.category = category;
	}
	public void setCreatedBy(String createdBy) {
		this.createdBy = createdBy;
	}
	public void setAddress(String address) {
		this.address = address;
	}
	public void setPhone(String phone) {
		this.phone = phone;
	}
	public void setDescr(String descr) {
		this.descr = descr;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public void setLat(double lat) {
		this.lat = lat;
	}
	public void setLon(double lon) {
		this.lon = lon;
	}
	public void setRating(int rating) {
		this.rating = rating;
	}
	public void setReview(String review) {
		this.review = review;
	}
	private String genPK(String name, String category) {
		// java version from the python code:
//	    while len(name) < 15:
//	        name = name + name
//	        
//	    key = binascii.hexlify("%d%s" % (CATEGORIES.index(category), name[0:15]))
//	    return str(uuid.UUID(key))
		while (name.length() < 15) {
			name = name + name;
		}
		name = name.substring(0,15);
		String cat = "";
		// hardcode indexOf
		if (category.compareTo("Recreational") == 0) {
			cat = "0";
		} else if (category.compareTo("Cultural") == 0) {
			cat = "1";
		} else if (category.compareTo("Historical") == 0) {
			cat = "2";
		} else 
			throw new IllegalArgumentException("Unknown category");
		
		String keyStr = cat + name;
        StringBuilder hexKey = new StringBuilder();
        
        for (int i=0; i < keyStr.length(); i++) {
        	if (i == 4 || i == 6 || i == 8 || i == 10) 
        		hexKey.append("-");
            hexKey.append(Integer.toHexString(keyStr.charAt(i)));
        }       
        
        // "0Far Corner Golf" should be 30466172-2043-6f72-6e65-7220476f6c66
        //System.err.println(keyStr);
        keyStr = hexKey.toString();
	    //System.err.println(keyStr);
	   
	    return keyStr;
	}
	
	public String getResponse() {
		String key = this.genPK(this.name, this.category);
		HttpResponse response = null;
		HttpClient httpclient = new DefaultHttpClient();
		String url = "http://0.0.0.0:8080/t2d/" + key;
		try {
			HttpGet httpget = new HttpGet(url);
			response = httpclient.execute(httpget);
			HttpEntity resEntity = response.getEntity();

			EntityUtils.consume(resEntity);
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			httpclient.getConnectionManager().shutdown();
		}
		System.err.println(response.getStatusLine().toString());
		return response.getStatusLine().toString();
	}
}
