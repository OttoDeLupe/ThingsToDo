package things2dofixtures; 

import java.io.IOException;
import java.io.InputStream;
import java.util.*;
import java.lang.*;
import java.util.ArrayList;

import org.json.simple.*;
import static util.ListUtility.list; // from fitnesse jar
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.HttpEntity;
import org.apache.http.util.EntityUtils;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.commons.io.IOUtils;

public class ItemsNear {
	private String category;
	private double lat = 0.0;
	private double lon = 0.0;
	
	public ItemsNear(String cat, double lat, double lon){
		this.category = cat;
		this.lat = lat;
		this.lon = lon;
	}
	
	public List<Object> query() {
		StringBuffer url = new StringBuffer("http://0.0.0.0:8080/t2dList?");
		url.append("category="); url.append(this.category);
		url.append("&lat=");  	 url.append(this.lat);
		url.append("&lon=");     url.append(this.lon);
		
		HttpResponse response = null;
		HttpClient httpclient = new DefaultHttpClient();
		JSONArray json = null;
		

		try {
			HttpGet httpget = new HttpGet(url.toString());
			httpget.addHeader("accept", "application/json");
			
			response = httpclient.execute(httpget);
			if (response.getStatusLine().getStatusCode() != 200) {
				throw new RuntimeException("Failed : HTTP error code : "
						   + response.getStatusLine().getStatusCode());
			}
			
			HttpEntity entity = response.getEntity();
			if (entity != null) {
			    long len = entity.getContentLength();
			    if (len != -1 && len < 2048) {
			        System.err.println(EntityUtils.toString(entity));
			    } else {
			        InputStream instream = entity.getContent();
			        String responseJson = IOUtils.toString(instream, "UTF-8");
					json = (JSONArray) JSONValue.parse(responseJson);
			    }
			}
			
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			httpclient.getConnectionManager().shutdown();
		}
		
		ArrayList returnList = new ArrayList();
		for (int i = 0; i < json.size(); i++) {
			ArrayList attrList1 = new ArrayList();
			ArrayList attrList2 = new ArrayList();
			ArrayList itemList = new ArrayList();
			JSONObject obj = (JSONObject) json.get(i);
			attrList1.add("name");
			attrList1.add(obj.get("name"));
			attrList2.add("pk");
			attrList2.add(obj.get("pk"));
				
			itemList.add(attrList1);
			itemList.add(attrList2);
			returnList.add(itemList);
		}
		
		return returnList;
//		return list (
//				list (
//					list("name", "Far Corner Golf Course"), 
//					list("pk", "30466172-2043-6f72-6e65-7220476f6c66")
//					),
//				list(
//					list("name", "Harold Parker State Forest"), 
//					list("pk", "30486172-6f6c-6420-5061-726b65722053")
//					),
//				list(
//					list("name", "Weir Hill"), 
//					list("pk", "30576569-7220-4869-6c6c-576569722048")
//					),
//				list (
//					list("name", "Ward Reservation"),
//					list("pk", "30576172-6420-5265-7365-72766174696f")
//					)
//					);
		
	}
}



