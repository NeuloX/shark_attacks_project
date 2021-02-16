
var countries = [];
var arrayList = [];


  d3.json('/api')
    .then(function(data){
        //console.log(data[0].country);
        for (var i in data[0].case_number) {
          var my_api = data[0];
          var obj = {
                "case_number":my_api.case_number[i],
                "country":my_api.country[i],
                "year": my_api.year[i],
                "type": my_api.type[i],
                "species": my_api.species[i],
                "fatal": my_api.fatal[i],
        };
        arrayList.push(obj);
      }

      var myGeoJSON = {};
      myGeoJSON.type = "FeatureCollection";
      myGeoJSON.features = arrayList;

      // Create a custom filtering function
      function shark_filter(shark) {
        return shark.species  == "white shark";
      }
      var shark_filt = myGeoJSON.features.filter(shark_filter);
      var year_list = [1980,1990,2000,2010,2020];
      console.log(shark_filt);
      var testy= 0;

      for (var x in shark_filt){
          if (shark_filt[x].year < 1990 && shark_filt[x].year>1979){
            testy = ++testy;
          }
      }
      console.log(testy);
        });

