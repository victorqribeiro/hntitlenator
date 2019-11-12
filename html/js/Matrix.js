class Matrix {

	constructor(rows, cols, values = 0){
		this.rows = rows || 0;
		this.cols = cols || 0;
		if( values instanceof Array ){
			this.data = values.slice();
		}else if( values == "RANDOM" ){
			this.data = Array( this.rows * this.cols ).fill().map( _ => Math.random() * 2 - 1 );
		}else{
			this.data = Array( this.rows * this.cols ).fill( values );
		}
	}
	
	multiply(b){
	
		if( b.rows !== this.cols ){
			throw new Error('Cols from Matrix A different from Rows of Matrix B');
			return;
		}
		
		let result = new Matrix( this.rows, b.cols );
		
		for(let i = 0; i < this.rows; i++){
			for(let j = 0; j < b.cols; j++){
				let s = 0;
				for(let k = 0; k < this.cols; k++){
					s += this.data[ i * this.cols + k ] * b.data[ k * b.cols + j ];
				}
				result.data[ i * result.cols + j ] = s;
			}
		}
		return result;
	}

	transpose(){
		for(let i = 0; i < this.rows; i++){
			for(let j = 0; j < this.cols; j++){
				let temp = this.data[ i * this.cols + j ];
				this.data[ i * this.cols + j ] = this.data[ j * this.rows + i ];
				this.data[ j * this.rows + i ] = temp;
			}
		}
		let temp = this.cols;
		this.cols = this.rows;
		this.rows = temp;
	}

	add(a){
		if( this.rows != a.rows || this.cols != a.cols ){
			throw new Error('Cant add Matrix of different sizes!');
			return;
		}
		for(let i = 0; i < this.data.length; i++){
			this.data[i] += a.data[i];
		}
	}
	
	subtract(a){
		if( this.rows != a.rows || this.cols != a.cols ){
			throw new Error('Cant subtract Matrix of different sizes!');
			return;
		}
		for(let i = 0; i < this.data.length; i++){
			this.data[i] -= a.data[i];
		}
	}
	
	scalar(a){
		for(let i = 0; i < this.data.length; i++){
			this.data[i] *= a;
		}
	}

	hadamard(a){
		if( this.rows != a.rows || this.cols != a.cols ){
			throw new Error('Cant multiply Matrix of different sizes!');
			return;
		}
		for(let i = 0; i < this.data.length; i++){
			this.data[i] *= a.data[i];
		}
	}

	copy(){
		return new Matrix( this.rows, this.cols, this.data );
	}

	foreach( func ){
		for(let i = 0; i < this.data.length; i++){
			this.data[i] = func( this.data[i] );
		}
	}

}
