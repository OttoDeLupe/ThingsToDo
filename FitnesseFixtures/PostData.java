package things2dofixtures;

import java.io.IOException;
import java.io.StringWriter;
import java.io.UnsupportedEncodingException;
import org.json.simple.JSONObject;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class PostData {
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

	public PostData(){
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
	
	private String makePayload() {
		JSONObject obj=new JSONObject();
		if (this.name != null) 		obj.put("name", this.name);
		if (this.category != null) 	obj.put("category",this.category);
		if (this.createdBy != null) obj.put("createdBy",this.createdBy);
		if (this.address != null) 	obj.put("address", this.address);
		if (this.phone != null) 	obj.put("phone", this.phone);
		if (this.descr != null) 	obj.put("descr", this.descr);
		if (this.url != null) 		obj.put("url", this.url);
		if (this.email != null) 	obj.put("email", this.email);
		if (this.lat != 0.0) 		obj.put("lat", this.lat);
		if (this.lon != 0.0) 		obj.put("lon", this.lon);
		if (this.rating != 0) 		obj.put("rating", this.rating);
		if (this.review != null) 	obj.put("review", this.review);

		StringWriter out = new StringWriter();
		try {
			obj.writeJSONString(out);
		} catch (Exception e) {
			System.err.println(e);
			return "";
		}

		String jsonText = "";
		try {
			jsonText = out.toString();
		} catch (Exception e) {
			System.err.println(e);
		}
		return jsonText;
	}

	public String postResponse() {
		StringEntity payload = null;
		HttpResponse response = null;
		try {
			payload = new StringEntity(this.makePayload(), "UTF-8");
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		HttpClient httpclient = new DefaultHttpClient();
		try {
			HttpPost httppost = new HttpPost("http://0.0.0.0:8080/t2d/");

			payload.setContentType("text/plain");

			httppost.setEntity(payload);

			response = httpclient.execute(httppost);
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
