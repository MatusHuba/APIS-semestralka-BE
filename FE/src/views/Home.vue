<template>
  <div class="container">

    <div class="row">

      <div class="col">

        <form class="row">
          <div class="col-auto">
            <label for="actual-location" class="visually-hidden">Moja poloha</label>
            <input type="text" class="form-control" id="actual-location" placeholder="Zadajte svoju polohu...">
          </div>
          
          <div class="col-auto">
            <button type="submit" class="btn btn-primary mb-3">Nájsť odvoz</button>
          </div>

        </form>

      </div>

    </div>

    <div class="container" >
      <div class="row" v-for="row in rows" :key="String(row)">

        <div class="col" v-for="item in row" :key="String(item)">
          <div class="card text-center">
            <div class="card-header text-muted" >
              <span class="badge bg-success" v-if="!item.busy">Pripravený vyzdvihnúť ťa</span>
              <span class="badge bg-danger" v-else>Obsadený</span>
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ item.name }}</h5>
              <h6 class="card-text">{{ item.car }}</h6>
              <p class="card-text"><b>{{ item.spz }}</b></p>
              <button class="btn btn-sm btn-warning" v-if="!item.busy">Vyzdvihni ma!!!</button>
              <button class="btn btn-sm btn-warning" disabled v-else>Vyzdvihni ma!!!</button>
            </div>
          </div>
        </div>

      </div>
    </div>


  </div>
 
 

</template>

<script>
export default {
  data() {
    return {
      taxi: [
        {
          id: 1,
          name: "Ladislav",
          spz: "KE231PS",
          car: "Škoda Octavia",
          busy: false  
        },
        {
          id: 2,
          name: "Peter",
          spz: "KE381NO",
          car: "Dacia Logan",
          busy: true  
        },
        {
          id: 1,
          name: "Janko",
          spz: "KE397NC",
          car: "Peugeot 3008",
          busy: false  
        }
      ]
    }
  },
    computed: {
        rows() {
            var rows = []
            var itemsPerRow = 5
            // assuming passer is an array of items..
            var arr = this.taxi
            for (var i = 0; i<arr.length; i+=itemsPerRow){
                var row = []
                for (var z = 0; z<itemsPerRow; z++) {
                    if(arr[i + z] != undefined){

                      row.push(arr[i + z])
                    }
                }
                rows.push(row)
            }
            console.log(rows)
            return rows
        }
    }
};
</script>
